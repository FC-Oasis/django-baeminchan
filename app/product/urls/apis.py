from django.urls import path

from product import apis

urlpatterns = [
    path('<int:pk>/', apis.ProductDetail.as_view()),
    path('', apis.ProductList.as_view()),
    path('search/', apis.ProductSearch.as_view()),
    path('random/', apis.ProductRandom.as_view()),
    path('discount/', apis.ProductDiscount.as_view()),
]
