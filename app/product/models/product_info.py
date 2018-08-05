from django.db import models

from .category import Category


class Product(models.Model):
    # 기본정보
    name = models.CharField(max_length=250, unique=True)
    category = models.ForeignKey(Category, related_name='products', null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='product', blank=True)
    related_products = models.ManyToManyField('self', verbose_name='related products', blank=True, symmetrical=False)

    # 가격
    price = models.PositiveIntegerField(verbose_name='정가', default=0)
    discount_price = models.PositiveIntegerField(verbose_name='할인금액', default=0)
    sale_price = models.PositiveIntegerField(verbose_name='판매가격', default=0)
    point_amount = models.IntegerField(verbose_name='적립될 포인트', default=0)

    # 상품정보고시
    type = models.CharField(max_length=300, blank=True)
    supplier = models.CharField(max_length=100, blank=True)
    weight = models.IntegerField(default=0)
    materials = models.TextField()
    alert_allergy = models.TextField()

    # Stocks
    DELIVERY_DAY_CHOICES = (
        ('mon', '월요일'),
        ('tue', '화요일'),
        ('wed', '수요일'),
        ('thu', '목요일'),
        ('fri', '금요일'),
        ('sat', '토요일'),
        ('sun', '일요일'),

    )
    stock = models.IntegerField(blank=True)
    available = models.BooleanField(default=True)
    delivery_days = models.CharField(max_length=20, blank=True, null=True, choices=DELIVERY_DAY_CHOICES)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return '{}'.format(self.name)

