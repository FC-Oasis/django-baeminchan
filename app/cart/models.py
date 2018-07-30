from django.conf import settings
from django.db import models

from product.models import Product


class Cart(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # item = models.ManyToManyField(Product, on_delete=models.SET_NULL)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, verbose_name='cart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='product', on_delete=models.CASCADE)
    amount = models.IntegerField(blank=True)


class Wishlist(models.Model):
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Orderstatus(models.Model):
    STATUS_CHOICES = (
        ('processing', '제품준비중'),
    )
    status = models.CharField(default='processing', max_length=100, choices=STATUS_CHOICES)


class Order(models.Model):
    pass


