from django.contrib.auth import get_user_model
from rest_framework import serializers

from product.models import Product
from product.serializer import ProductSerializer
from ..models import Cart, CartItem
from members.serializers import UserSerializer
User = get_user_model()


class ProductForCartSerializer(ProductSerializer):
    productimage_set = None

    class Meta:
        model = Product
        fields = (
            'id',
            'raw_name',
            'sale_price',
            'thumbnail_url1',

        )
        read_only_fields = (
            'raw_name',
            'sale_price',
            'thumbnail_url1',
        )


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductForCartSerializer()

    class Meta:
        model = CartItem
        fields = (
            'pk',
            'product',
            'amount',
            'item_total_price',
        )

    def create(self, validated_data):
        product = validated_data['product']
        amount = validated_data['amount']
        cart, cart_created = Cart.objects.get_or_create(user=self.context['request'].user)
        cart_item, cart_item_created = CartItem.objects.get_or_create(
            product=product,
            defaults={
                'cart': cart,
                'amount': amount,
            }
        )
        if cart_item_created is False:
            cart_item.amount += amount
            cart_item.save()
        return cart_item

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
            'total_point',
            'total_price',
            'shipping_fee',
            'total_order_price',
        )


# new
class CartItemAddSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = CartItem
        fields = (
            'pk',
            'product',
            'amount',
            'item_total_price',
        )

    def create(self, validated_data):
        product = validated_data['product']
        amount = validated_data['amount']
        cart, cart_created = Cart.objects.get_or_create(user=self.context['request'].user)
        cart_item, cart_item_created = CartItem.objects.get_or_create(
            product=product,
            defaults={
                'cart': cart,
                'amount': amount,
            }
        )
        if cart_item_created is False:
            cart_item.amount += amount
            cart_item.save()
        return cart_item

    def update(self, instance, validated_data):
        instance.amount = validated_data.get('amount', instance.amount)
        instance.save()
        return instance


class CartAddSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    cart_items = CartItemAddSerializer(many=True)

    class Meta:
        model = Cart
        fields = (
            'user',
            'cart_items',
            'total_point',
            'total_price',
            'shipping_fee',
            'total_order_price',
        )

