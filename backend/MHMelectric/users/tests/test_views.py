from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.authtoken.models import Token
from urllib.parse import urlencode

from users.views import register_user, delete_token, admin_create_user, admin_get_user, get_token_from_api_key, get_user_info, get_car_info_from_user


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_user_url = reverse('register_user')
        self.delete_token_url = reverse('delete_token')
        self.admin_create_user_url = reverse('admin_create_user', args=['some-username1', 'test-password'])
        self.admin_get_user_url = reverse('admin_get_user', args=['some-username1'])

    def test_register_user(self):
        response = self.client.post(self.register_user_url, {
            'username': 'some-username',
            'email': 'someemail@example.com',
            'password': 'somerandompassword',
            'password2': 'somerandompassword'
        })

        user = User.objects.get(username='some-username')
        token = Token.objects.get(user=user).key

        self.assertEquals(response.status_code, 200)
        self.assertDictEqual(response.data, {
            'response': 'Successfully created a new user.',
            'email': user.email,
            'username': user.username,
            'token': token
        })

    def test_delete_token(self):
        user, _ = User.objects.get_or_create(username='some-username1')
        token, _ = Token.objects.get_or_create(user=user)
        response = self.client.post(self.delete_token_url, HTTP_X_OBSERVATORY_AUTH=token.key)

        user = User.objects.get(username='some-username1')
        count_token = len(Token.objects.filter(user=user))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(count_token, 0)

    def test_admin_create_userFAIL(self):
        user, _ = User.objects.get_or_create(username='some-username1')
        token, _ = Token.objects.get_or_create(user=user)
        response = self.client.post(self.admin_create_user_url, HTTP_X_OBSERVATORY_AUTH=token.key)

        self.assertEquals(response.status_code, 401)
        self.assertDictEqual(response.data, {
            'Failed': 'Not authorized'
        })

    def test_admin_create_userSUCCESS(self):
        admin, _ = User.objects.get_or_create(username='some-admin', is_superuser=True)
        token, _ = Token.objects.get_or_create(user=admin)
        response = self.client.post(self.admin_create_user_url, HTTP_X_OBSERVATORY_AUTH=token.key)

        self.assertEquals(response.status_code, 200)
        self.assertDictEqual(response.data, {
            'Success': 'User some-username1 created'
        })


        # Test behavior when user already exists
        response = self.client.post(self.admin_create_user_url, HTTP_X_OBSERVATORY_AUTH=token.key)

        self.assertEquals(response.status_code, 200)
        self.assertDictEqual(response.data, {
            'Success': 'Password updated for some-username1'
        })

    def test_admin_get_userFAIL(self):
        user, _ = User.objects.get_or_create(username='some-username1')
        token, _ = Token.objects.get_or_create(user=user)
        response = self.client.get(self.admin_get_user_url, HTTP_X_OBSERVATORY_AUTH=token.key)

        self.assertEquals(response.status_code, 401)
        self.assertDictEqual(response.data, {
            'Failed': 'Not authorized'
        })

    def test_admin_get_userSUCCESS(self):
        admin, _ = User.objects.get_or_create(username='some-admin', is_superuser=True)
        token, _ = Token.objects.get_or_create(user=admin)
        response = self.client.get(self.admin_get_user_url, HTTP_X_OBSERVATORY_AUTH=token.key)

        self.assertEquals(response.status_code, 402)
        self.assertEquals(response.data, {'No data'})


        # Test behavior when user already exists
        user, _ = User.objects.get_or_create(username='some-username1')
        user.email = "some-username1@email.com"
        user.save()
        response = self.client.get(self.admin_get_user_url, HTTP_X_OBSERVATORY_AUTH=token.key)

        self.assertEquals(response.status_code, 200)
        self.assertDictEqual(response.data, {
            'username': 'some-username1',
            'email': 'some-username1@email.com'
        })
