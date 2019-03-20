from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class TestPostWomanCRUDWithoutAuthentication(APITestCase):
    def setUp(self):
        self.url = '/api/postwoman/'

    def test_try_create_postwoman_without_user_return_forbidden(self):
        data = {'name': 'Name1', 'max_distance': 1}
        request = self.client.post(self.url, data)

        expected = 403
        self.assertEqual(expected, request.status_code)


class TestPostWomanCRUDWithAuthentication(APITestCase):
    def setUp(self):
        self.username = 'usernaname'
        self.password = 'password'
        user = User.objects.create_user(
            username=self.username, password=self.password)
        user.save()
        self.client.login(username=self.username, password=self.password)
        self.url = '/api/postwoman/'

    def test_create_new_postwoman_with_all_data_return_sucess(self):
        data = {'name': 'Name1', 'max_distance': 1}
        request = self.client.post(self.url, data)

        expected = 201
        self.assertEqual(expected, request.status_code)
        self.assertEqual(data, request.data)

    def test_create_new_postwoman_without_max_distance_return_sucess(self):
        data = {'name': 'Name1'}
        request = self.client.post(self.url, data)

        expected = 201
        expected_data = {'name': 'Name1', 'max_distance': 10.0}
        self.assertEqual(expected, request.status_code)
        self.assertEqual(expected_data, request.data)

    def test_try_create_duplicate_postwoman_return_error(self):
        data = {'name': 'Name1'}
        self.client.post(self.url, data)
        request = self.client.post(self.url, data)

        expected = 400
        self.assertEqual(expected, request.status_code)
