from django.urls import path

from .. import apis
from ..apis import kakao

urlpatterns = [
    path('', apis.UserList.as_view()),
    path('create/', apis.UserCreate.as_view()),
    path('<int:pk>/', apis.UserDetail.as_view()),
    path('kakao/', kakao.kakao_login, name='kakao-login'),
]
