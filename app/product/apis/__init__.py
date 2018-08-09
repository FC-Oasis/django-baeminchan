from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializer import ProductSerializer
from ..models import Product


class ProductDetail(APIView):

    def get(self, request, pk, format=None):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)

        return Response(serializer.data)
