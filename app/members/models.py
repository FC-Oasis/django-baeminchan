from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    fullname = models.CharField(verbose_name='이름',
                                max_length=100,
                                help_text='필수입력')
    jibun_address = models.CharField(max_length=100,
                                     blank=True,
                                     verbose_name='지번 주소',
                                     help_text='선택입력')
    road_address = models.CharField(max_length=100,
                                    blank=True,
                                    verbose_name='도로명 주소',
                                    help_text='선택입력')
    contact_phone = models.CharField(max_length=150,
                                     default="",
                                     verbose_name='전화번호',
                                     help_text='필수입력, {3}-{4}-{4}형식만 허용')
    birthday = models.DateField(null=True,
                                blank=True,
                                verbose_name='생년월일',
                                help_text='필수입력')
    # 초대코드
