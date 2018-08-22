from django.urls import path

from cart.apis.order import UserOrderCreateList, UserOrderDetail
from ..apis.carts import CartList, UserCart, UserCartItemList, UserCartItemDetail

urlpatterns = [
    path('list/', CartList.as_view()),
    path('usercart/', UserCart.as_view()),
    path('cartitemlist/', UserCartItemList.as_view()),
    path('cartitemdetail/<int:pk>/', UserCartItemDetail.as_view()),
    path('userorder/', UserOrderCreateList.as_view()),
    path('userorderdetail/<int:pk>/', UserOrderDetail.as_view()),

]
