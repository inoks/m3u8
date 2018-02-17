from django.test import TestCase
from django.test import Client


class AppTestCase(TestCase):
    def test_true(self):
        self.assertTrue(True)


class URLsTesting(TestCase):

    def setUp(self):
        self.donald_trump = Client(enforce_csrf_checks=True)
        self.ok = (200, 302)

    def test_urls(self):

        urls = ('/', '/admin/', '/add/', '/channel/new/',
                '/channels', '/accounts/login/',
                '/accounts/logout/', )

        for url in urls:
            response = self.donald_trump.get(url)
            self.assertIn(response.status_code, self.ok, msg='Path: %s, Status code: %s,' %
                                                             (response.request['PATH_INFO'], response.status_code))
