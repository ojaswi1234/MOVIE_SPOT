from django.urls import include, path
from .views import landingPage, movieDetails

urlpatterns= [
    path("", landingPage,name="landing"),
    path("movie/<int:movie_id>/", movieDetails , name="movie_details"),
]