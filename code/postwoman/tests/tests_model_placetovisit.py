from urllib.parse import urljoin

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from model_mommy import mommy


class TestPlaceToVisitCRUDWithoutAuthentication(APITestCase):
    def setUp(self):
        self.url = '/api/placetovisit/'

    def test_try_create_postwoman_without_user_return_forbidden(self):
        data = {'name': 'Name1'}
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
        self.url = '/api/placetovisit/'
        self.base_postwoman_url = '/api/postwoman/{id}/'

    def test_create_new_placetovist_with_all_data_return_sucess(self):
        postwoman = mommy.make('postwoman.PostWoman')
        data = {
            'name': 'Name1', 'latitude': 1, 'longitude': 2,
            'postwoman': self.base_postwoman_url.format(id=postwoman.id)}
        request = self.client.post(self.url, data)

        expected = 201
        url = urljoin('http://testserver/',
                      self.base_postwoman_url.format(id=postwoman.id))
        expected_data = {
            'name': 'Name1', 'latitude': 1, 'longitude': 2,
            'postwoman': url, 'visited': False}
        self.assertEqual(expected, request.status_code)
        self.assertEqual(expected_data, request.data)

    def test_create_new_placetovisit_without_coordinates_return_sucess(self):
        postwoman = mommy.make('postwoman.PostWoman')
        data = {
            'name': 'Name1',
            'postwoman': self.base_postwoman_url.format(id=postwoman.id)}
        request = self.client.post(self.url, data)

        expected = 201
        url = urljoin('http://testserver/',
                      self.base_postwoman_url.format(id=postwoman.id))
        expected_data = {
            'name': 'Name1', 'latitude': 0, 'longitude': 0,
            'postwoman': url, 'visited': False}
        self.assertEqual(expected, request.status_code)
        self.assertEqual(expected_data, request.data)

    def test_try_create_duplicate_placetovist_return_error(self):
        postwoman = mommy.make('postwoman.PostWoman')
        data = {
            'name': 'Name1',
            'postwoman': self.base_postwoman_url.format(id=postwoman.id)}
        self.client.post(self.url, data)
        request = self.client.post(self.url, data)

        expected = 400
        self.assertEqual(expected, request.status_code)
