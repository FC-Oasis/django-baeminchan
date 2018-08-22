from rest_framework import generics, permissions

from ..serializers.order import OrderSerializer
from ..models import Order


class UserOrderCreateList(generics.ListCreateAPIView):
    """
    reqeust.user의 order list를 반환
    """
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = OrderSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        queryset = Order.objects.all()
        return queryset.filter(user=self.request.user)


class UserOrderDetail(generics.RetrieveUpdateAPIView):
    """
    request.user의 order 한개의 정보를 반환
    """
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = OrderSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        queryset = Order.objects.all()
        return queryset.filter(user=self.request.user)

