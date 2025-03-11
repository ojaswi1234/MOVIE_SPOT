from django.urls import include, path
from .views import landingPage

urlpatterns= [
    path("", landingPage,name="landing")
]