from rest_framework import serializers

from product.models import Product
from ..models import Cart, CartItem
from members.serializers import UserSerializer


class ProductDetailForCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'pk',
            'name',
            'sale_price',
        )


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductDetailForCartSerializer()
    class Meta:
        model = CartItem
        fields = (
            'product',
        )


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    cart_items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = (
            'user',
            'cart_items',
            'total_price',
        )
        read_only_fields = ('user', )

