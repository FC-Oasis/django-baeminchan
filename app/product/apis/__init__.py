import random

from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from ..pagination import ProductListResultsSetPagination
from ..serializer import ProductSerializer, ProductSimpleSerializer
from ..models import Product, ParentCategory, Category


class ProductDetail(APIView):

    def get(self, request, pk, format=None):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)

        return Response(serializer.data)


class ProductList(generics.ListAPIView):
    serializer_class = ProductSimpleSerializer
    pagination_class = ProductListResultsSetPagination

    def get_queryset(self):
        queryset = Product.objects.all()
        parent_category_name = self.request.query_params.get('parent_category', None)
        category_name = self.request.query_params.get('category', None)
        parent_category = get_object_or_404(
            ParentCategory,
            name=parent_category_name,
        )
        if category_name == '전체보기':
            queryset = queryset.filter(category__parent_category__name=parent_category_name)
        else:
            category = get_object_or_404(
                Category,
                parent_category=parent_category,
                name=category_name,
            )
            if category is not None:
                queryset = queryset.filter(category=category)
        return queryset


class ProductRandom(generics.ListAPIView):
    serializer_class = ProductSimpleSerializer

    def get_queryset(self):
        pk_list = list(range(1, Product.objects.all().count() + 1))
        random_pk = []
        for i in range(12):
            random_pk.append(pk_list.pop(random.randint(0, len(pk_list))))
        print(random_pk)
        queryset = Product.objects.filter(pk__in=random_pk)
        return queryset


class ProductSearch(generics.ListAPIView):
    serializer_class = ProductSimpleSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(raw_name__contains=self.request.query_params.get('query', ''))
        if not queryset:
            raise Http404
        return queryset
