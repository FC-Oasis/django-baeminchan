from rest_framework import serializers

from ..models import CartItem, Order, Cart
from ..serializers.carts import CartItemSerializer


class OrderSerializer(serializers.ModelSerializer):
    order_items = CartItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            'pk',
            'ordered_at',
            'order_items',
            'order_status',
            'payment_price',
        )

    def create(self, validated_data):
        status = validated_data['order_status']
        user = self.context['request'].user
        order = Order.objects.create(
            user=user,
            order_status=status,
        )
        for cartitem in CartItem.objects.filter(cart__user=user):
            cartitem.cart = None
            cartitem.order = order
            cartitem.save(force_update=True)
        return order

    def update(self, instance, validated_data):
        status = validated_data['order_status']
        instance.order_status = status
        instance.save()
        return instance
