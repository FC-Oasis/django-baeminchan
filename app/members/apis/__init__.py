from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import UserSerializer, PasswordChangeSerializer, EmailChangeSerializer

User = get_user_model()


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreate(generics.CreateAPIView):
    permission_classes = (
        permissions.AllowAny,
    )
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DeleteUser(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
