from django.urls import include, path

from .views import Login, RegisterUser

urlpatterns= [
    path("login/", Login.as_view(), name="login"),
    path("register/", RegisterUser.as_view(), name="register"),
]