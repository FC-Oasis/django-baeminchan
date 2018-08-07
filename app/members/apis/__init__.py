from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import generics, permissions, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import UserSerializer, PasswordChangeSerializer, EmailChangeSerializer, ContactPhoneChangeSerializer

User = get_user_model()


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreate(generics.CreateAPIView):
    permission_classes = (
        permissions.AllowAny,
    )
    serializer_class = UserSerializer


class UserDetail(mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PasswordChange(generics.UpdateAPIView):
    model = User
    permission_classes = (
        IsAuthenticated,
    )
    serializer_class = PasswordChangeSerializer

    def get_object(self):
        return self.request.user


class EmailChange(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (
        IsAuthenticated,
    )
    serializer_class = EmailChangeSerializer


class ContactPhoneChange(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (
        IsAuthenticated,
    )
    serializer_class = ContactPhoneChangeSerializer
