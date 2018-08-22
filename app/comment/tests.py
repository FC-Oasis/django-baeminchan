from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from members.tests import get_dummy_user_info
from product.models import Product

User = get_user_model()


class CommentTest(APITestCase):
    URL = '/api/comments/'

    def test_comment_create(self):
        product = Product.objects.create(stock=10)
        user = User.objects.create_user(**get_dummy_user_info())

        self.client.force_authenticate(user=user)
        response = self.client.post(
            self.URL,
            data={
                'product': product.id,
                'content': 'hello',
                'rating': 4,
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_comment_list(self):
        product1 = Product.objects.create(stock=10)
        product2 = Product.objects.create(stock=10)
        user = User.objects.create_user(**get_dummy_user_info())

        self.client.force_authenticate(user=user)
        for product in Product.objects.all():
            self.client.post(
                self.URL,
                data={
                    'product': product.id,
                    'content': 'hello',
                    'rating': 4,
                }
            )

        self.client.force_authenticate()
        response1 = self.client.get(
            self.URL,
            data={
                'product_id': product1.id,
            }
        )

        response2 = self.client.get(
            self.URL,
            data={
                'product_id': product2.id,
            }
        )

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertTrue(response1.json())
        self.assertNotEqual(response1, response2)

        response = self.client.get(
            self.URL,
            data={
                'product_id': 99999,
            }
        )

        self.assertEqual(response.json(), {'detail': '찾을 수 없습니다.'})

    def test_comment_put(self):
        product = Product.objects.create(stock=10)
        user = User.objects.create_user(**get_dummy_user_info())

        self.client.force_authenticate(user=user)
        response_prev = self.client.post(
            self.URL,
            data={
                'product': product.id,
                'content': 'hello',
                'rating': 4,
            }
        )

        comment_id = response_prev.json()['id']
        response = self.client.put(
            self.URL + f'{comment_id}/',
            data={
                'product': product.id,
                'content': 'world',
                'rating': 3,
            }
        )

        self.assertNotEqual(response_prev.json(), response.json())

        self.client.force_authenticate()
        response = self.client.put(
            self.URL + f'{comment_id}/',
            data={
                'product': product.id,
                'content': 'world',
                'rating': 3,
            }
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json(),
            {'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'},
        )

    def test_comment_delete(self):
        product = Product.objects.create(stock=10)
        user = User.objects.create_user(**get_dummy_user_info())

        self.client.force_authenticate(user=user)

        response_prev = self.client.post(
            self.URL,
            data={
                'product': product.id,
                'content': 'hello',
                'rating': 4,
            }
        )

        comment_id = response_prev.json()['id']

        self.client.force_authenticate()
        response = self.client.delete(
            self.URL + f'{comment_id}/',
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.json(),
            {'detail': '자격 인증데이터(authentication credentials)가 제공되지 않았습니다.'},
        )

        self.client.force_authenticate(user=user)
        response = self.client.delete(
            self.URL + f'{comment_id}/',
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
