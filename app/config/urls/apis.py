from django.urls import path, include

urlpatterns = [
    path('users/', include('members.urls.apis')),
]
