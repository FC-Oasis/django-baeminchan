from django.conf import settings
from django.db import models

from .order import Order
from product.models import Product


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 배송비, 적립금

    @property
    def total_price(self, total_price=0):
        for item in self.cart_items.all():
            total_price += item.item_total_price
        return total_price


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
    amount = models.PositiveIntegerField(default=1)

    @property
    def item_total_price(self):
        return self.amount * self.product.sale_price
