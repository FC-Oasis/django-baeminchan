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
        random_pk_list = []
        categories = ParentCategory.objects.values_list('pk', flat=True)

        for parent_category in categories:
            pk_list = list(Product.objects.filter(category__parent_category=parent_category).values_list('pk', flat=True))
            for i in range(12):
                random_pk_list.append(pk_list.pop(pk_list.index(random.choice(pk_list))))
        qs = Product.objects.filter(pk__in=random_pk_list).select_related('category__parent_category').order_by('id')
        return qs


class ProductSearch(generics.ListAPIView):
    serializer_class = ProductSimpleSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(raw_name__contains=self.request.query_params.get('query', ''))
        if not queryset:
            raise Http404
        return queryset
