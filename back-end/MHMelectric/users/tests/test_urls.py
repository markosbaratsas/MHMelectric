from django.test import SimpleTestCase
from django.urls import reverse, resolve
from rest_framework.authtoken.views import obtain_auth_token

from users.views import register_user, delete_token, admin_create_user, admin_get_user, ObtainAPIKey, cli_logout, get_token_from_api_key, user_info, get_car_info_from_user


class TestUserUrls(SimpleTestCase):

    def test_register(self):
        url = reverse('register_user')
        self.assertEquals(resolve(url).func, register_user)

    def test_login(self):
        url = reverse('obtain_auth_token')
        self.assertEquals(resolve(url).func, obtain_auth_token)

    def test_logout(self):
        url = reverse('delete_token')
        self.assertEquals(resolve(url).func, delete_token)

    def test_admin_create_user(self):
        url = reverse('admin_create_user', args=['some-username', 'some-password'])
        self.assertEquals(resolve(url).func, admin_create_user)

    def test_admin_get_user(self):
        url = reverse('admin_get_user', args=['some-username'])
        self.assertEquals(resolve(url).func, admin_get_user)

    def test_cli_login(self):
        url = reverse('ObtainAPIKey')
        self.assertEquals(resolve(url).func.view_class, ObtainAPIKey)

    def test_cli_logoutr(self):
        url = reverse('cli_logout')
        self.assertEquals(resolve(url).func, cli_logout)

    def test_get_token_from_api_key(self):
        url = reverse('get_token_from_api_key')
        self.assertEquals(resolve(url).func, get_token_from_api_key)

    def test_get_user_info(self):
        url = reverse('get_user_info')
        self.assertEquals(resolve(url).func, user_info)

    def test_get_car_info_from_user(self):
        url = reverse('get_car_info_from_user')
        self.assertEquals(resolve(url).func, get_car_info_from_user)
