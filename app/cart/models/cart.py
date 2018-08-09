from django.conf import settings
from django.db import models

from .order import Order
from product.models import Product


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField(default=0)
    # 배송비, 적립금


class CartItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='cart_items',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    cart = models.ForeignKey(
        Cart,
        related_name='cart_items',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    product = models.ForeignKey(
        Product,
        related_name='product_in_cart',
        on_delete=models.CASCADE,
        blank=True,
    )
    item_price = models.PositiveIntegerField(default=0, blank=True)
    amount = models.PositiveIntegerField(default=1)
