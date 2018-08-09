from django.conf import settings
from django.db import models
from django.utils import timezone




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

