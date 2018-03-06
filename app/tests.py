from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase, Client

from app.models import Channel, Playlist
from app import forms


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

    def test_form(self):

        add_playlist = self.client.post(reverse('create-playlist'), data={'path': 'https://dailyiptvlist.com/dl/fr-m3uplaylist-2018-03-06.m3u'})
        self.assertEqual(add_playlist.status_code, 200)

        new_channel = self.client.post(reverse('new-channel'), data={'path': 'https://archive.org/download/fluxustv/Fluxus_TV.mp4', 'title': 'Simple',
                                                                     'group': 'first'})
        self.assertEqual(new_channel.status_code, 302)

        update_channel = self.client.post(reverse('channel', args=[1]), data={'path': 'https://archive.org/download/fluxustv/Fluxus_TV.mp4', 'title': 'Complicated',
                                                                              'group': 'changed'})
        self.assertEqual(update_channel.status_code, 302)


class FormTestCase(TestCase):

    def setUp(self):

        self.channel_data = {

            'title': 'Simple Title',
            'path': 'forest',
            'group': 'Second',
            'hidden': True

        }

        self.playlist_data = {

            'url': 'https://m3u8.ru/',
            'remove_existed': True

        }

    def test_channel_create(self):
        form = forms.ChannelCreateForm(self.channel_data)
        self.assertTrue(form.is_valid())

    def test_channel_update(self):
        form = forms.ChannelUpdateForm(self.channel_data)
        self.assertTrue(form.is_valid())

    def test_playlist(self):
        form = forms.PlaylistForm(self.playlist_data)
        self.assertTrue(form.is_valid())
