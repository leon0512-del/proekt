import os

import requests

OMDB_API_KEY = os.getenv("OMDB_API_KEY", "")

def get_movie_by_title(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def generate_movie_hints(movie_data):
    # Initial hints from API data
    return [
        f"Released in {movie_data.get('Year')}",
        f"Genre: {movie_data.get('Genre')}",
        f"Directed by {movie_data.get('Director')}"
    ]
