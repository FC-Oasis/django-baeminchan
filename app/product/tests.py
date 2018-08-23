from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase


class ProductTest(APITestCase):
    URL = '/api/products/'

    def test_product_random_status_code(self):
        response = self.client.get(
            self.URL + 'random/',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            self.URL + 'random/'
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
