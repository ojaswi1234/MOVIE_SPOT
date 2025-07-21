from django.shortcuts import render
from django.conf import settings
import requests
from django.contrib.auth.decorators import login_required
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json

# Set up logging
logger = logging.getLogger(__name__)

API_KEY = settings.TMDB_API_KEY

# Configure requests session with retries
session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

# Create your views here.
def landingPage(request):
    return render(request, 'movies/landing_page.html')

@login_required(login_url='/user/login/')
def moviePage(request):
    category = request.GET.get('category', 'popular')
    search_query = request.GET.get('search', '')
    page = int(request.GET.get('page', 1))
    next_page = page + 1

    base_url = "https://api.themoviedb.org/3/movie/"
    if search_query:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={search_query}&page={page}"
    else:
        url = f"{base_url}{category}?api_key={API_KEY}&page={page}"

    try:
        response = session.get(url, timeout=10)
        logger.debug(f"Request URL: {url} | Status Code: {response.status_code}")
        response.raise_for_status()
        data = response.json()
        movies = data.get('results', [])
        total_pages = data.get('total_pages', 1)
        has_next_page = page < total_pages
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        movies = []
        has_next_page = False
        error_message = "Unable to fetch movies. Please check your internet connection or try again later."
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        movies = []
        has_next_page = False
        error_message = "Invalid response from the movie database. Please try again later."

    context = {
        'movies': movies,
        'category': category,
        'search_query': search_query,
        'error_message': error_message if movies == [] else None,
        'page': page,
        'next_page': next_page if has_next_page else None,
    }

    if request.headers.get("HX-Request"):
        return render(request, 'movies/partials/_movies_list.html', context)
    return render(request, 'movies/movie_page.html', context)

@login_required(login_url='/user/login/')
def movieDetails(request, movie_id):
    movie_detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    movie_credit_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}"
    movie_trailer_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}"

    data = credits_data = trailers = None
    error_message = None

    try:
        # Fetch movie details
        response = session.get(movie_detail_url, timeout=10)
        logger.debug(f"Movie details URL: {movie_detail_url} | Status Code: {response.status_code}")
        response.raise_for_status()
        data = response.json()

        # Fetch credits
        movie_credit_response = session.get(movie_credit_url, timeout=10)
        logger.debug(f"Credits URL: {movie_credit_url} | Status Code: {movie_credit_response.status_code}")
        movie_credit_response.raise_for_status()
        credits_data = movie_credit_response.json()

        # Fetch trailers
        trailer_response = session.get(movie_trailer_url, timeout=10)
        logger.debug(f"Trailers URL: {movie_trailer_url} | Status Code: {trailer_response.status_code}")
        trailer_response.raise_for_status()
        trailer_data = trailer_response.json().get('results', [])
        trailers = [video for video in trailer_data if video.get('site') == 'YouTube' and video.get('type') == 'Trailer']

    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        error_message = "Unable to fetch movie details. Please check your internet connection or try again later."
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        error_message = "Invalid response from the movie database. Please try again later."

    return render(request, 'movies/movie_details.html', {
        'movie': data or {},
        'credits': credits_data or {},
        'trailers': trailers or [],
        'error_message': error_message,
    })