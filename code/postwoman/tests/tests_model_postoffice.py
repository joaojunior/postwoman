from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class TestPostOfficeCRUDWithoutAuthentication(APITestCase):
    def setUp(self):
        self.url = '/api/postoffice/'

    def test_try_create_letter_without_user_return_forbidden(self):
        data = {'name': 'postoffice', 'latitude': 0, 'longitude': 0}
        request = self.client.post(self.url, data)

        expected = 403
        self.assertEqual(expected, request.status_code)


class TestPostOfficeCRUDWithAuthentication(APITestCase):
    def setUp(self):
        self.username = 'usernaname'
        self.password = 'password'
        user = User.objects.create_user(
            username=self.username, password=self.password)
        user.save()
        self.client.login(username=self.username, password=self.password)
        self.url = '/api/postoffice/'

    def test_create_new_postoffice_with_only_name_return_sucess(self):
        data = {'name': 'postoffice'}
        request = self.client.post(self.url, data)

        expected = 201
        self.assertEqual(expected, request.status_code)

    def test_try_create_postoffice_duplicate_return_error(self):
        data = {'name': 'postoffice'}
        self.client.post(self.url, data)
        request = self.client.post(self.url, data)

        expected = 400
        self.assertEqual(expected, request.status_code)

    def test_create_new_postoffice_with_all_fields_return_sucess(self):
        data = {'name': 'postoffice', 'latitude': 1, 'longitude': 2}
        request = self.client.post(self.url, data)

        expected = 201
        self.assertEqual(expected, request.status_code)
