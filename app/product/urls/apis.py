from django.urls import path

from product import apis

urlpatterns = [
    path('<int:pk>/', apis.ProductDetail.as_view()),
    path('', apis.ProductList.as_view()),
    path('search/', apis.ProductSearch.as_view())
]
