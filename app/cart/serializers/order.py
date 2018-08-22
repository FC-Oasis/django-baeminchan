from rest_framework import serializers

from ..models import CartItem, Order
from ..serializers.carts import CartItemSerializer


class OrderSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            'pk',
            'cart_items',
            'order_status',
        )

    def create(self, validated_data):
        status = validated_data['order_status']
        order = Order.objects.create(
            user=self.context['request'].user,
            order_status=status,
        )
        for cartitem in CartItem.objects.filter(cart__user=self.context['request'].user):
            cartitem.cart = None
            cartitem.order = order
            cartitem.save()
        return order

    def update(self, instance, validated_data):
        status = validated_data['order_status']
        instance.order_status = status
        instance.save()
        return instance
