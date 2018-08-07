from django.urls import path, include

from ..views import views
from .. import apis
from ..apis import kakao

urlpatterns = [
    path('', apis.UserList.as_view()),
    path('create/', apis.UserCreate.as_view()),
    path('<int:pk>/', apis.UserDetail.as_view()),
    path('kakao/', kakao.kakao_login, name='kakao-login'),
    path('delete/<int:pk>/', apis.UserDetail.as_view()),
    path('change/', include([
        path('email/<int:pk>/', apis.EmailChange.as_view()),
        path('password/<int:pk>/', apis.PasswordChange.as_view()),
        path('contact_phone/<int:pk>/', apis.ContactPhoneChange.as_view()),
    ])),
    path('auth-token/', apis.AuthToken.as_view()),
    path('auth-test/', apis.AuthenticationTest.as_view()),
]
