from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status, mixins
from rest_framework.authtoken.models import Token
from rest_framework.compat import authenticate
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.urls import logout
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


class PasswordChange(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def patch(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(request.user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.is_valid(raise_exception=True))


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


class AuthToken(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            token, __ = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
            }
            return Response(data)
        raise AuthenticationFailed('인증정보가 올바르지 않습니다')


class AuthenticationTest(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response(UserSerializer(request.user).data)
        raise NotAuthenticated('로그인 상태가 아닙니다')


class Logout(APIView):
    """
    유저 객체를 받아 쿼리셋에 담고,
    request 받은 유저의 auth_token이 맞으면 로그아웃을 시켜줌
    """
    queryset = User.objects.all()

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response("로그아웃 성공", status=status.HTTP_200_OK)
