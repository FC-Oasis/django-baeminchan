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
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True, null=True)
    order_status = models.CharField(default='processing',
                                    max_length=200,
                                    choices=STATUS_CHOICES)

    @property
    def payment_price(self, payment_price=0):
        for item in self.order_items.all():
            payment_price += item.item_total_price
        if payment_price <= 40000:
            return payment_price+2500
        return payment_price

    @property
    def created_at_korean_time(self):
        korean_timezone = timezone(settings.TIME_ZONE)
        return self.ordered_at.astimezone(korean_timezone)