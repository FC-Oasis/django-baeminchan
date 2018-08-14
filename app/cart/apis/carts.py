from rest_framework import generics

from ..models import Cart
from ..serializers.carts import CartSerializer


class CartList(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class UserCart(generics.ListAPIView):
    """
    pk가 일치하는 user의 cart정보를 보여줌
    """
    serializer_class = CartSerializer

    def get_queryset(self):
        queryset = Cart.objects.all()
        return queryset.filter(user__pk=self.kwargs.get('pk'))

