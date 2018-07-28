from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    full_name = models.CharField(verbose_name='user_name', max_length=100, unique=True)
    address = models.ManyToManyField(
        'Address', related_name='user_addresses'
    )
    contact_phone = models.CharField(max_length=150, default="")
    birthday = models.CharField(max_length=200, default="")
    # 초대코드


class Address(models.Model):
    zonecode = models.CharField(max_length=20)
    postcode = models.CharField(max_length=20)
    roadAddress = models.CharField(max_length=300)
    jibunAddress = models.CharField(max_length=300)
