from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    fullname = models.CharField(verbose_name='user_name', max_length=100)
    jibun_address = models.CharField(max_length=100, blank=True,)
    road_address = models.CharField(max_length=100, blank=True,)
    contact_phone = models.CharField(max_length=150, default="")
    birthday = models.DateField(null=True, blank=True)
    # 초대코드
