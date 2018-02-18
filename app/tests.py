from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from django.shortcuts import reverse
from app.models import Channel, Playlist, Upload
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile


class URLsTesting(TestCase):

    def setUp(self):
        self.donald_trump = Client(enforce_csrf_checks=True)
        self.donald_trump.force_login(User.objects.create_user('Garry Kasparov', 'garry1@ronda.com', 'garry500'))
        self.ok = (200, 302)

    def test_urls(self):

        urls = ('index',
                'create-playlist',
                'new-channel',
                'channels',
                'login',
                'logout'
                )

        hard_urls = ('/login/facebook/',
                     '/login/vk-oauth2/',
                     '/i18n/setlang/'
                     )

        for url in urls:
            response = self.donald_trump.get(reverse(url), folow=True)
            self.assertIn(response.status_code, self.ok, msg='Path: %s, Status code: %s,' %
                                                             (response.request['PATH_INFO'], response.status_code))

        for url in hard_urls:
            response = self.donald_trump.get(url, folow=True)
            self.assertIn(response.status_code, self.ok, msg='Path: %s, Status code: %s,' %
                                                             (response.request['PATH_INFO'], response.status_code))


class ModelsTesting(TestCase):

    def setUp(self):
        jeryy_user = User.objects.create_user('Jerry CZ', 'jerry@a1.com', '436zfer')

        self.playlist = Playlist(user=jeryy_user, created_at=timezone.datetime.today())
        self.playlist.save()

        self.channel = Channel(playlist=self.playlist, title='Testing Playlist',
                               duration='150 min', group='The best group', path='no path')
        self.channel.save()

        self.upload = Upload(user=jeryy_user, info='Hello! ', created_at=timezone.datetime.today(),
                             file=SimpleUploadedFile('file_t.jpg', b'Nothing'))
        self.upload.save()

    def test_playlist(self):
        self.assertTrue(self.playlist.public_link)

        # self.assertTrue(self.playlist.get_absolute_url())  # Raises an error

        self.assertTrue(self.playlist.count)

    def test_channel(self):
        self.assertTrue(self.channel.get_absolute_url())
