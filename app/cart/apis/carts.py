
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from members.models import User
from product.models import Product
from ..models import Cart, CartItem
from ..serializers.carts import CartSerializer, CartItemSerializer


class CartList(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class UserCart(generics.RetrieveUpdateAPIView):
    """
    pk가 일치하는 user의 cart정보를 보여줌
    """
    serializer_class = CartSerializer

    def get_queryset(self):
        queryset = Cart.objects.all()
        return queryset.filter(user__pk=self.kwargs.get('pk'))

