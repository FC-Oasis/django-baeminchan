from django.conf import settings
from django.db import models

from product.models import Product


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField(default=0)
    # 배송비, 적립금


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, verbose_name='cart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='product', on_delete=models.CASCADE)
    product_price = models.PositiveIntegerField(default=0)
    product_amount = models.IntegerField(blank=True)


