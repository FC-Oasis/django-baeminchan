from django.contrib.auth import get_user_model
from rest_framework import serializers

from product.models import Product
from ..models import Cart, CartItem
from members.serializers import UserSerializer
User = get_user_model()


class ProductDetailForCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'pk',
            'name',
            'sale_price',
        )
        read_only_fields = ('sale_price', )


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductDetailForCartSerializer()

    class Meta:
        model = CartItem
        fields = (
            'pk',
            'product',
            'amount',
            'item_total_price',
        )

    def update(self, instance, validated_data):
        instance.amount = validated_data.get('amount', instance.amount)
        instance.save()
        return instance


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
