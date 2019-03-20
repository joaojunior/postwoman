from urllib.parse import urljoin

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from model_mommy import mommy


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
        self.base_postoffice_url = '/api/postoffice/{id}/'

    def test_create_new_postwoman_with_all_data_return_sucess(self):
        postoffice = mommy.make('postwoman.PostOffice')
        data = {
            'name': 'Name1', 'max_distance': 1,
            'postoffice': self.base_postoffice_url.format(id=postoffice.id)}
        request = self.client.post(self.url, data)

        expected = 201
        url = urljoin('http://testserver/',
                      self.base_postoffice_url.format(id=postoffice.id))
        expected_data = {
            'name': 'Name1', 'max_distance': 1, 'postoffice': url}
        self.assertEqual(expected, request.status_code)
        self.assertEqual(expected_data, request.data)

    def test_create_new_postwoman_without_max_distance_return_sucess(self):
        postoffice = mommy.make('postwoman.PostOffice')
        data = {
            'name': 'Name1',
            'postoffice': self.base_postoffice_url.format(id=postoffice.id)}
        request = self.client.post(self.url, data)

        expected = 201
        url = urljoin('http://testserver/',
                      self.base_postoffice_url.format(id=postoffice.id))
        expected_data = {
            'name': 'Name1', 'max_distance': 10.0, 'postoffice': url}
        self.assertEqual(expected, request.status_code)
        self.assertEqual(expected_data, request.data)

    def test_try_create_duplicate_postwoman_return_error(self):
        postoffice = mommy.make('postwoman.PostOffice')
        data = {
            'name': 'Name1',
            'postoffice': self.base_postoffice_url.format(id=postoffice.id)}
        self.client.post(self.url, data)
        request = self.client.post(self.url, data)

        expected = 400
        self.assertEqual(expected, request.status_code)
