from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializer import ProductSerializer, ProductSimpleSerializer
from ..models import Product, ParentCategory, Category


class ProductDetail(APIView):

    def get(self, request, pk, format=None):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)

        return Response(serializer.data)


class ProductList(generics.ListAPIView):
    serializer_class = ProductSimpleSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        parent_category = get_object_or_404(
            ParentCategory,
            name=self.request.query_params.get('parent_category', None),
        )
        category = get_object_or_404(
            Category,
            parent_category=parent_category,
            name=self.request.query_params.get('category', None),
        )
        if category is not None:
            queryset = queryset.filter(category=category)
        return queryset


class ProductSearch(generics.ListAPIView):
    serializer_class = ProductSimpleSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(raw_name__contains=self.request.query_params.get('query', ''))
        if not queryset:
            raise Http404
        return queryset
