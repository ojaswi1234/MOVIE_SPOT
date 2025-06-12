from django.urls import include, path
from .views import landingPage, movieDetails, moviePage

urlpatterns= [
    path("", landingPage,name="landing"),
    path("movie/", moviePage, name="movie_page"),
    path("movie/<int:movie_id>/", movieDetails , name="movie_details"),
]