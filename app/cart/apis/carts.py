
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


class UserCartItemList(generics.ListCreateAPIView):
    """
    pk가 일치하는 user의 cart에 담긴 아이템리스트를 보여줌
    """
    serializer_class = CartItemSerializer

    def get_queryset(self):
        queryset = CartItem.objects.all()
        user_pk = self.kwargs.get('user_pk')
        user = get_object_or_404(User, id=user_pk)
        cart = get_object_or_404(
            Cart,
            user=user,
        )
        return queryset.filter(cart=cart)

    def post(self, request, *args, **kwargs):
        user_pk = self.kwargs.get('user_pk')
        user = get_object_or_404(User, id=user_pk)
        cart = get_object_or_404(
            Cart,
            user=user,
        )
        product_name = request.data.get('product.name')
        product = Product.objects.get(name=product_name)
        amount = request.data.get('amount')
        cartitem = CartItem.objects.create(cart=cart, product=product, amount=amount)
        serializer = CartItemSerializer(cartitem)
        return Response(serializer.data)


class UserCartItemDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    pk가 일치하는 user의 cart에 담긴 아이템을 보여줌
    """
    serializer_class = CartItemSerializer

    def get_queryset(self):
        queryset = CartItem.objects.all()
        user_pk = self.kwargs.get('user_pk')
        user = get_object_or_404(User, id=user_pk)
        cart = get_object_or_404(
            Cart,
            user=user,
        )
        return queryset.filter(cart=cart)
