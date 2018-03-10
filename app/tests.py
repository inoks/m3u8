import requests_mock
import requests

from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase, Client

from app.models import Channel, Playlist


class AppTestCase(TestCase):
    def setUp(self):
        self.username = 'John Doe'
        self.email = 'john@example.com'
        self.password = 'dolphins'
        self.user = get_user_model().objects.create_user(
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

    def test_form1(self):
        default = 'mock://127.0.0.1:8000'

        new_channel_url = default + reverse('new-channel')
        create_playlist_url = default + reverse('create-playlist')
        update_channel_url = default + reverse('channel', args=[1])

        adapter = requests_mock.Adapter()

        adapter.register_uri('POST', new_channel_url, text='Ok')
        adapter.register_uri('POST', create_playlist_url, text='Ok')
        adapter.register_uri('POST', update_channel_url, text='Ok')

        session = requests.session()
        session.mount('mock', adapter)

        for url in (new_channel_url, create_playlist_url, update_channel_url):
            response = session.post(url)
            self.assertEqual(response.content, b'Ok')
