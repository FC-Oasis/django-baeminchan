from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import generics, permissions, status, mixins
from rest_framework.authtoken.models import Token
from rest_framework.compat import authenticate
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
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


class DeleteToken(APIView):
    """
    유저 객체를 받아 쿼리셋에 담고,
    get 요청을 보내서 request로 토큰값이 확인되면 토큰값을 삭제하고
    Response로 200을 보내줌
    """
    queryset = User.objects.all()

    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
