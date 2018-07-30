from django.contrib.auth import get_user_model, authenticate, login
from django.http import HttpResponse

User = get_user_model()


def kakao_login(request):
    code = request.GET.get('code')
    user = authenticate(request, code=code)
    if user is not None:
        login(request, user)
        msg = f'<h1>카카오톡 로그인 성공 : {user.full_name}<h1>'
        return HttpResponse(msg)
    return HttpResponse('<h1>카카오톡 로그인 실패<h1>')
