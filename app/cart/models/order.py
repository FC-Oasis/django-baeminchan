from django.conf import settings
from django.db import models
from django.utils import timezone

from product.models import Product


class Order(models.Model):
    STATUS_CHOICES = (
        ('processing', '제품준비중'),
        ('shipping', '배송중'),
        ('abandon', '주문취소'),
        ('finish', '배송완료'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # created = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(default='processing', max_length=200, choices=STATUS_CHOICES)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    product_amount = models.PositiveIntegerField(default=1)
