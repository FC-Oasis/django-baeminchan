from django.contrib.auth import get_user_model, authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()


class AuthToken(APIView):
    def post(self, request):
        access_token = request.data.get('access_token')
        user = authenticate(request, access_token=access_token)

        if user:
            token, __ = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
            }
            return Response(data)
        raise AuthenticationFailed('인증정보가 올바르지 않습니다')
