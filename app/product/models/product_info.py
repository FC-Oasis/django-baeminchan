from statistics import mean

from django.db import models

from .category import Category


class Product(models.Model):
    # 기본정보
    raw_name = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    category = models.ForeignKey(Category, related_name='products', null=True, on_delete=models.SET_NULL)
    description = models.TextField(null=True, blank=True)
    thumbnail_url1 = models.URLField(blank=True)
    thumbnail_url2 = models.URLField(blank=True, null=True)
    thumbnail_url3 = models.URLField(blank=True, null=True)
    thumbnail_url4 = models.URLField(blank=True, null=True)
    thumbnail_url5 = models.URLField(blank=True, null=True)
    thumbnail_url6 = models.URLField(blank=True, null=True)
    # related_products = models.ManyToManyField('self', verbose_name='related products', blank=True, symmetrical=False)

    # 가격
    price = models.PositiveIntegerField(verbose_name='정가', default=0)
    discount_rate = models.PositiveIntegerField(verbose_name='할인율', default=0)
    sale_price = models.PositiveIntegerField(verbose_name='판매가격', default=0)
    point_amount = models.IntegerField(verbose_name='적립될 포인트', default=0)

    # 상품정보고시
    type = models.TextField()
    supplier = models.CharField(max_length=100, blank=True)
    weight = models.IntegerField(default=0)
    materials = models.TextField()
    alert_allergy = models.TextField()

    # Stocks
    stock = models.IntegerField(blank=True)
    available = models.BooleanField(default=True)
    delivery_days = models.CharField(max_length=50, blank=True)
    delivery_type = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return '{}'.format(self.raw_name)

    @property
    def related_products(self):
        return Product.objects.filter(supplier=self.supplier)

    def avg_rating(self):
        rating_list = list(self.comment_set.all().values_list('rating'))
        if rating_list:
            return mean(rating_list)
        else:
            return 0

    def comment_count(self):
        return self.comment_set.count()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return '{}'.format(self.image_url)
