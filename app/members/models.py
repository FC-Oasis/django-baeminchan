from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    fullname = models.CharField(verbose_name='user_name', max_length=100)
    jibun_address = models.CharField(max_length=100, blank=True,)
    road_address = models.CharField(max_length=100, blank=True,)
    contact_phone = models.CharField(max_length=150, default="")
    birthday = models.DateField(max_length=200, default="")
    # 초대코드
