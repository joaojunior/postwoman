from urllib.parse import urljoin

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from model_mommy import mommy


class TestRouteCRUDWithoutAuthentication(APITestCase):
    def setUp(self):
        self.url = '/api/placetovisit/'

    def test_try_create_route_without_user_return_forbidden(self):
        data = {'route': '{}'}
        request = self.client.post(self.url, data)

        expected = 403
        self.assertEqual(expected, request.status_code)


class TestRouteCRUDWithAuthentication(APITestCase):
    def setUp(self):
        self.username = 'usernaname'
        self.password = 'password'
        user = User.objects.create_user(
            username=self.username, password=self.password)
        user.save()
        self.client.login(username=self.username, password=self.password)
        self.url = '/api/route/'
        self.base_postwoman_url = '/api/postwoman/{id}/'

    def test_create_new_route_with_all_data_return_sucess(self):
        postwoman = mommy.make('postwoman.PostWoman')
        data = {
            'date': '1942-12-01', 'route': '{}',
            'postwoman': self.base_postwoman_url.format(id=postwoman.id)}
        request = self.client.post(self.url, data)

        expected = 201
        url = urljoin('http://testserver/',
                      self.base_postwoman_url.format(id=postwoman.id))
        route = {'route': [(str(postwoman.postoffice.id), 'PostOffice', 0)],
                 'total_cost': 0}
        expected_data = {
            'date': '1942-12-01', 'route': route,
            'postwoman': url}
        self.assertEqual(expected, request.status_code)
        self.assertEqual(expected_data, request.data)

    def test_create_new_route_without_postwoman_return_error(self):
        data = {'date': '1942-12-01', 'route': '{}'}
        request = self.client.post(self.url, data)

        expected = 400
        self.assertEqual(expected, request.status_code)

    def test_try_create_duplicate_route_return_error(self):
        postwoman = mommy.make('postwoman.PostWoman')
        data = {
            'date': '1942-12-01', 'route': '{}',
            'postwoman': self.base_postwoman_url.format(id=postwoman.id)}
        self.client.post(self.url, data)
        request = self.client.post(self.url, data)

        expected = 400
        self.assertEqual(expected, request.status_code)
