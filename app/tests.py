import logging

import requests_mock
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import QueryDict
from django.shortcuts import reverse
from django.test import Client, RequestFactory
from django.test import TestCase
from django.core.paginator import Paginator
from django.http.request import HttpRequest

from app.models import Channel, Playlist
from app.templatetags.extra_tags import url_replace, ellipsis_or_number
from app.utils import M3U8ChannelProxy, load_m3u8_from_file, load_remote_m3u8


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
            playlist=self.playlist,
            title='Testing Playlist',
            duration='150',
            group='The best group',
            path='no path'
        )

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
        channel_string = 'EXTINF:-1,RTV 4 HD'
        channel = M3U8ChannelProxy(channel_string)
        self.assertEqual('-1', channel.duration)
        self.assertEqual('RTV 4 HD', channel.title)

    def test_simple_extinf_without_title(self):
        channel_string = 'EXTINF:25,'
        channel = M3U8ChannelProxy(channel_string)
        self.assertEqual('25', channel.duration)
        self.assertEqual('', channel.title)

    def test_complex_extinf(self):
        channel_string = 'EXTINF:-1 ' \
                         'tvg-id="12" ' \
                         'tvg-name="Cinema Pro ARB" ' \
                         'tvg-logo="http://m3u8.ru/logo.png" ' \
                         'group-title="Arab Countries",Cinema Pro ARB'
        channel = M3U8ChannelProxy(channel_string)
        self.assertEqual('-1', channel.duration,)
        self.assertEqual('Cinema Pro ARB', channel.title, )
        self.assertEqual('12', channel.extra_data['tvg-ID'])
        self.assertEqual('Cinema Pro ARB', channel.extra_data['tvg-name'])
        self.assertEqual('http://m3u8.ru/logo.png', channel.extra_data['tvg-logo'])
        self.assertEqual('Arab Countries', channel.extra_data['group-title'])

    def test_bad_extinf(self):
        channel_string = 'EXTINF:Cool, but no duration'
        channel = M3U8ChannelProxy(channel_string)
        self.assertFalse(channel.is_valid)

    def test_url_replace_tags(self):

        factory = RequestFactory()
        request = factory.get('/list/?q=HD&page=2')
        res_url_query = QueryDict(url_replace(request, 'page', 3))

        self.assertEqual({'q': 'HD', 'page': '3'}, res_url_query.dict())

        request = factory.get('/list')
        res_url = url_replace(request, 'page', 3)

        self.assertEqual('page=3', res_url)

    def test_ellipsis_or_number(self):
        paginator = Paginator([x for x in range(1000)], 50)
        page_count = paginator.num_pages

        request = HttpRequest()

        request.GET['page'] = 1
        chosen_page = request.GET['page']

        for page in range(1, page_count):
            for current_page in range(page_count):
                if current_page == chosen_page:
                    self.assertEqual(ellipsis_or_number(paginator, current_page, request), chosen_page)
                    continue
                if current_page in (chosen_page + 3, chosen_page - 3):
                    self.assertEqual(ellipsis_or_number(paginator, current_page, request), '...')
                    continue

                if current_page in (chosen_page + 1, chosen_page + 2, chosen_page - 1,
                                    chosen_page - 2, paginator.num_pages, paginator.num_pages - 1, 1, 2):
                    self.assertEqual(ellipsis_or_number(paginator, current_page, request), current_page)
                    continue
            request.GET['page'] += 1
            chosen_page = request.GET['page']
