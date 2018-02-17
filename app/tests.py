from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User


class URLsTesting(TestCase):

    def setUp(self):
        self.donald_trump = Client(enforce_csrf_checks=True)
        self.donald_trump.force_login(User.objects.create_superuser('Garry Kasparov', 'garry1@ronda.com', 'garry500'))
        self.ok = (200, 302)

    def test_urls(self):

        urls = ('/',
                '/admin/',
                '/add/',
                '/channel/new/',
                '/channels',
                '/accounts/login/',
                '/accounts/logout/',
                '/login/facebook/',
                '/login/vk-oauth2/',
                '/i18n/setlang/',
                )

        for url in urls:
            response = self.donald_trump.get(url, folow=True)
            self.assertIn(response.status_code, self.ok, msg='Path: %s, Status code: %s,' %
                                                             (response.request['PATH_INFO'], response.status_code))
