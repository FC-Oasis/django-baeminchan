from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from product.models import Product

User = get_user_model()


class CartItemTest(APITestCase):
    URL = '/api/carts/cartitemlist/'

    def tests_cart_item_create(self):
        user = User.objects.create_user(username='dummy')
        product = Product.objects.create(
            raw_name='raw_name',
            name='name',
            price=100,
            materials='materials',
            alert_allergy='alert_allergy',
            stock=10,
        )
        data = {
            'product': product.pk,
            'amount': 5,
        }
        self.client.force_authenticate(user=user)
        response = self.client.post(self.URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class UserCartGetTest(APITestCase):
    URL = '/api/carts/usercart/'

    def test_cart_create(self):
        user = User.objects.create_user(username='dummy')
        self.client.force_authenticate(user=user)
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

