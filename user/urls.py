from django.urls import include, path

from .views import Login

urlpatterns= [
    path("login/", Login.as_view(), name="login"),
]