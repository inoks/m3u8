import logging

from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import Client
from django.test import TestCase

from app.models import Channel, Playlist
from app.utils import M3U8Channel


class AppTestCase(TestCase):
    def setUp(self):
        self.username, self.password, self.email = 'John Doe', 'dolphins', 'john@example.com'

        self.user = User.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

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


class M3U8TestCase(TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)

    def test_simple_extinf(self):
        channel_string = 'EXTINF:-1,RTV 4 HD'
        channel = M3U8Channel(channel_string)
        self.assertEqual('-1', channel.duration)
        self.assertEqual('RTV 4 HD', channel.title)

    def test_simple_extinf_without_title(self):
        channel_string = 'EXTINF:25,'
        channel = M3U8Channel(channel_string)
        self.assertEqual('25', channel.duration)
        self.assertEqual('', channel.title)

    def test_complex_extinf(self):
        channel_string = 'EXTINF:-1 ' \
                         'tvg-id="12" ' \
                         'tvg-name="Cinema Pro ARB" ' \
                         'tvg-logo="http://m3u8.ru/logo.png" ' \
                         'group-title="Arab Countries",Cinema Pro ARB'
        channel = M3U8Channel(channel_string)
        self.assertEqual('-1', channel.duration,)
        self.assertEqual('Cinema Pro ARB', channel.title, )
        self.assertEqual('12', channel.extra_data['tvg-ID'])
        self.assertEqual('Cinema Pro ARB', channel.extra_data['tvg-name'])
        self.assertEqual('http://m3u8.ru/logo.png', channel.extra_data['tvg-logo'])
        self.assertEqual('Arab Countries', channel.extra_data['group-title'])

    def test_bad_extinf(self):
        channel_string = 'EXTINF:Cool, but no duration'
        channel = M3U8Channel(channel_string)
        self.assertFalse(channel.is_valid)
