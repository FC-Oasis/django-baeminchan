from rest_framework import generics

from ..models import Cart
from ..serializers.carts import CartSerializer


class CartList(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer



