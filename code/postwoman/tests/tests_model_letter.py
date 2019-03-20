from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from model_mommy import mommy


class TestLetterCRUDWithoutAuthentication(APITestCase):
    def setUp(self):
        self.url = '/api/letter/'

    def test_try_create_letter_without_user_return_forbidden(self):
        data = {'latitude': 0, 'longitude': 0}
        request = self.client.post(self.url, data)

        expected = 403
        self.assertEqual(expected, request.status_code)


class TestLetterCRUDWithAuthentication(APITestCase):
    def setUp(self):
        self.username = 'usernaname'
        self.password = 'password'
        user = User.objects.create_user(
            username=self.username, password=self.password)
        user.save()
        self.client.login(username=self.username, password=self.password)
        self.url = '/api/letter/'
        self.base_postwoman_url = '/api/postwoman/{id}/'

    def test_create_new_letter_with_only_postwoman_return_sucess(self):
        postwoman = mommy.make('postwoman.PostWoman')
        data = {'postwoman': self.base_postwoman_url.format(id=postwoman.id)}
        request = self.client.post(self.url, data)

        expected = 201
        self.assertEqual(expected, request.status_code)

    def test_try_create_letter_duplicate_return_error(self):
        postwoman = mommy.make('postwoman.PostWoman')
        data = {'postwoman': self.base_postwoman_url.format(id=postwoman.id)}
        self.client.post(self.url, data)
        request = self.client.post(self.url, data)

        expected = 400
        self.assertEqual(expected, request.status_code)

    def test_create_new_letter_with_all_fields_return_sucess(self):
        postwoman = mommy.make('postwoman.PostWoman')
        data = {
            'latitude': 1, 'longitude': 2, 'date': '2019-03-20',
            'delivered': False,
            'postwoman': self.base_postwoman_url.format(id=postwoman.id)}
        request = self.client.post(self.url, data)

        expected = 201
        self.assertEqual(expected, request.status_code)
