from django.urls import include, path

from .views import ContactView, Login, RegisterUser, Logout

urlpatterns= [
    path("login/", Login.as_view(), name="login"),
    path("register/", RegisterUser.as_view(), name="register"),
    path("logout/", Logout.as_view(), name="logout"),
    path("contact/", ContactView.as_view(), name="contact"),
    
]