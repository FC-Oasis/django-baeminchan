from django.urls import path

from ..apis.carts import CartList, UserCart, UserCartItemList, UserCartItemDetail

urlpatterns = [
    path('list/', CartList.as_view()),
    path('usercart/', UserCart.as_view()),
    path('cartitemlist/', UserCartItemList.as_view()),
    path('cartitemdetail/<int:user_pk>/<int:pk>/', UserCartItemDetail.as_view()),
]
