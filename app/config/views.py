from django.http import HttpResponse


def index(request):
    return HttpResponse('<h1>[패스트캠퍼스 WPS 8기 1팀] 배민찬 카피 서버<h1>')
