from django.shortcuts import render
from django.conf import settings
import requests
from django.contrib.auth.decorators import login_required

API_KEY = settings.TMDB_API_KEY

# Create your views here.
def landingPage(request):
    return render(request, 'movies/landing_page.html')
   

   
@login_required(login_url='/user/login/')
def moviePage(request):
    category = request.GET.get('category', 'popular')
    search_query = request.GET.get("search", "")
    page = int(request.GET.get('page', 1))
    next_page = page + 1

    print(f'API_KEY: {API_KEY}')  # Debug print statement to verify API key
    base_url = "https://api.themoviedb.org/3/movie/"

    if search_query:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={search_query}&page={page}"
    else:
        url = f"{base_url}{category}?api_key={API_KEY}&page={page}"

    try:
        response = requests.get(url)
        print(f'Status Code: {response.status_code}')
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json().get('results', [])
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        data = []

    error_message = f"Oops!! Something went wrong!"

    if request.headers.get("HX-Request"):
        return render(request, 'movies/partials/_movies_list.html', {
            'movies': data,
            'category': category,
            'search_query': search_query,
            'error_message': error_message,
            'page': page,
            'next_page': next_page
        })

    return render(request, 'movies/movie_page.html', {
        'movies': data,
        'category': category,
        'search_query': search_query,
        'error_message': error_message,
        'page': page,
        'next_page': next_page
    })




def movieDetails(request, movie_id):
    movie_detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    movie_credit_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}"
    movie_trailer_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={API_KEY}"
    error_message = None
    try:
        movie_credit_response = requests.get(movie_credit_url)
        movie_credit_response.raise_for_status()  # Raise an error for bad status codes
        credits_data = movie_credit_response.json() 
        response = requests.get(movie_detail_url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        trailer_response = requests.get(movie_trailer_url)
        trailer_response.raise_for_status()  # Raise an error for bad status codes
        trailer_data = trailer_response.json().get('results', [])

        trailers = [video for video in trailer_data if video.get('site') == 'YouTube' and video.get('type') == 'Trailer']
        
    except requests.exceptions.RequestException as e:
        data =[]
        trailers = []
        credits_data = []
        trailer_data = []

        error_message = f"Oops!! Something went wrong!"

    return render(request, 'movies/movie_details.html', {"movie": data, error_message: error_message, "credits": credits_data, "trailers": trailers})

