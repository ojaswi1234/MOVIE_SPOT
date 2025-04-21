from django.shortcuts import render
from django.conf import settings
import requests

# Create your views here.
def landingPage(request):
    API_KEY = settings.TMDB_API_KEY
    category = request.GET.get('category', 'popular')
    search_query = request.GET.get("search","")
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
    return render(request, 'movies/landing_page.html', {
        'movies': data,
        'category': category,
        'search_query': search_query,
        'error_message': error_message,
        'page': page,
        'next_page': next_page
    })