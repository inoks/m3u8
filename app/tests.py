import logging

import requests_mock
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import QueryDict
from django.shortcuts import reverse
from django.test import Client, RequestFactory
from django.test import TestCase

from app.models import Channel, Playlist
from app.templatetags.extra_tags import url_replace
from app.utils import M3U8ChannelFactory, load_m3u8_from_file, load_remote_m3u8


class AppTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(AppTestCase, cls).setUpClass()

        logging.disable(logging.CRITICAL)

    def setUp(self):
        self.username = 'John Doe'
        self.email = 'john@example.com'
        self.password = 'dolphins'
        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )
        self.client = Client()
        self.client.login(
            username=self.username,
            password=self.password
        )

        self.anonymous_client = Client()

        self.playlist = Playlist(user=self.user)
        self.playlist.save()

        self.channel = Channel.objects.create(
            user=self.user,
            title='Testing Playlist',
            duration='150',
            group='The best group',
            path='no path'
        )
        self.channel.playlists.add(self.playlist)

        self.sample_m3u8 = '\n'.join([
            '#EXTM3U',
            '#EXTINF:0,BBC NEWS',
            '#EXTGRP:News',
            'http://example.com/bbc-news-tv.m3u8',
            '#EXTINF:0,Fox NEWS',
            '#EXTGRP:News',
            'http://example.com/fox-news-tv.m3u8',
            '#EXTINF:Invalid channel',
            'http://example.com/invalid-channel.m3u8'
        ])

    def test_urls(self):
        urls = [
            'index',
            'create-playlist',
            'new-channel',
            'channels',
            'login',
            'logout'
        ]

        social_auth_redirect_urls = [
            '/login/facebook/',
            '/login/vk-oauth2/',
        ]

        for url in urls:
            response = self.client.get(reverse(url), follow=True)
            self.assertEqual(response.status_code, 200, msg='Unable to open: %s' % url)

        for url in social_auth_redirect_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302, msg='Unable to open: %s' % url)

    def test_playlist(self):
        self.assertGreater(self.playlist.count, 0)

    def test_playlist_public_link(self):
        self.assertIsNotNone(self.playlist.public_link)

        response = self.client.get(self.playlist.public_link)
        self.assertEqual(response.status_code, 200)

    def test_channel_link(self):
        self.assertIsNotNone(self.channel.get_absolute_url())

    def test_channel_update(self):
        response = self.client.get(self.channel.get_absolute_url())
        self.assertEqual(response.status_code, 200)

        response = self.anonymous_client.get(self.channel.get_absolute_url())
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url, msg='Not redirected to login view')

    def test_load_from_file(self):
        m3u8_file = SimpleUploadedFile(
            "playlist.m3u8",
            str.encode(self.sample_m3u8),
            content_type='application/x-mpegURL'
        )
        load_m3u8_from_file(m3u8_file, self.playlist, remove_existed=True)

        self.assertEqual(self.playlist.count, 2)

    @requests_mock.mock()
    def test_load_remote_m3u8(self, m):

        mocked_path = 'http://example.com/playlist.m3u8'
        m.get(mocked_path, text=self.sample_m3u8)

        load_remote_m3u8(mocked_path, self.playlist, remove_existed=True)

        self.assertEqual(self.playlist.count, 2)

    def test_simple_extinf(self):
        channel_string = '#EXTINF:-1,RTV 4 HD'
        chf = M3U8ChannelFactory()
        chf.process_line(channel_string)
        self.assertEqual('-1', chf.duration)
        self.assertEqual('RTV 4 HD', chf.title)

    def test_bytestring_extinf(self):
        channel_string = b'#EXTINF:-1 tvg-id="Omreop Fryslan NL" tvg-name="Omrop Fryslan NL" ' \
                         b'tvg-logo="http://1.1.1.1/picons/omropfryslannl.png" ' \
                         b'group-title="Netherland",Omrop Fryslan NL'
        chf = M3U8ChannelFactory()
        chf.process_line(channel_string)
        self.assertEqual('-1', chf.duration)
        self.assertEqual('Netherland', chf.extra_data.get('group-title'))
        self.assertEqual('Omreop Fryslan NL', chf.extra_data.get('tvg-ID'))
        self.assertEqual('Omrop Fryslan NL', chf.extra_data.get('tvg-name'))
        self.assertEqual('http://1.1.1.1/picons/omropfryslannl.png', chf.extra_data.get('tvg-logo'))

    def test_simple_extinf_without_title(self):
        channel_string = '#EXTINF:25,'
        chf = M3U8ChannelFactory()
        chf.process_line(channel_string)
        self.assertEqual('25', chf.duration)
        self.assertEqual('', chf.title)

    def test_complex_extinf(self):
        channel_string = '#EXTINF:-1 ' \
                         'tvg-id="12" ' \
                         'tvg-name="Cinema Pro ARB" ' \
                         'tvg-logo="http://m3u8.ru/logo.png" ' \
                         'group-title="Arab Countries",Cinema Pro ARB'
        chf = M3U8ChannelFactory()
        chf.process_line(channel_string)
        self.assertEqual('-1', chf.duration,)
        self.assertEqual('Cinema Pro ARB', chf.title, )
        self.assertEqual('12', chf.extra_data['tvg-ID'])
        self.assertEqual('Cinema Pro ARB', chf.extra_data['tvg-name'])
        self.assertEqual('http://m3u8.ru/logo.png', chf.extra_data['tvg-logo'])
        self.assertEqual('Arab Countries', chf.extra_data['group-title'])

    def test_bad_extinf(self):
        channel_string = '#EXTINF:Cool, but no duration'
        chf = M3U8ChannelFactory()
        chf.process_line(channel_string)

        self.assertFalse(chf.is_complete())

    def test_url_replace_tags(self):

        factory = RequestFactory()
        request = factory.get('/list/?q=HD&page=2')
        res_url_query = QueryDict(url_replace(request, 'page', 3))

        self.assertEqual({'q': 'HD', 'page': '3'}, res_url_query.dict())

        request = factory.get('/list')
        res_url = url_replace(request, 'page', 3)

        self.assertEqual('page=3', res_url)
