from django.urls import path

from product import apis

urlpatterns = [
    path('<int:pk>/', apis.ProductDetail.as_view()),
]
