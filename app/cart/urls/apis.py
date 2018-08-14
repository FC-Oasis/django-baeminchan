from django.urls import path

from ..apis.carts import CartList, UserCart

urlpatterns = [
    path('list/', CartList.as_view()),
    path('usercart/<int:pk>/', UserCart.as_view()),
]
