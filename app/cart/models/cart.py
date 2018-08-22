from django.conf import settings
from django.db import models

from .order import Order
from product.models import Product


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    # 적립금
    @property
    def total_point(self, total_point=0):
        for item in self.cart_items.all():
            total_point += (item.product.point_amount*item.amount)
        return total_point

    # 총상품금액
    @property
    def total_price(self, total_price=0):
        for item in self.cart_items.all():
            total_price += item.item_total_price
        return total_price

    # 배송비
    @property
    def shipping_fee(self, shipping_fee=2500):
        if self.total_price >= 40000:
            shipping_fee = 0
        return shipping_fee

    # 총주문금액
    @property
    def total_order_price(self):
        total_order_price = self.total_price+self.shipping_fee
        return total_order_price


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
