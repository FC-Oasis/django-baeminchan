from django.urls import path

from ..apis.carts import CartList

urlpatterns = [
    path('list/', CartList.as_view()),
]