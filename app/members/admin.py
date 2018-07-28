from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from members.models import User


admin.site.register(User)
