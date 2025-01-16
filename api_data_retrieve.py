import requests
import json
from create_db_script import db, cursor

# OUR DBMS PROJECT: best 1000 comedy movies of all times (full-length, English, US)

'''
General Settings
'''
API_KEY = '82cd47774ed6c624ce7b0e24a89048c3'  # your API key from TMDB website
BASE_URL = 'https://api.themoviedb.org/3/'
OUTPUT_FILE = 'movies.json'
GENRE_ID = 35  # Genre ID for comedy movies
LANG = 'en'
REGION = 'US'

'''
Movie Handling
'''

def fetch_movies(page):
    url = BASE_URL + 'discover/movie'
    params = {
        'api_key': API_KEY,
        'with_genres': GENRE_ID,
        'language': LANG,
        'with_original_language': LANG,
        'with_runtime.gte': 70,
        'region': REGION,
        'sort_by': 'vote_average.desc',
        'vote_count.gte': 500,
        'page': page,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if page == 1:
            print(f"Found {data['total_results']} Movies")
        return data
    else:
        print("Error: Failed to fetch data: " + str(response.status_code))
        return None

def insert_movie(movie):
    # insert movie into movie table
    movie_query = """INSERT INTO movie (title, release_year, runtime, overview, popularity, votes_average, votes_count)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    values = (
        movie.get('title'),
        movie.get('release_date')[:4],
        movie.get('runtime'),
        movie.get('overview'),
        movie.get('popularity'),
        movie.get('vote_average'),
        movie.get('vote_count')
    )
    cursor.execute(movie_query, values)
    db.commit()

    # Insert genres into movie_genre table
    genre_query =  """INSERT INTO movie_genre (movie_id, genre_id)
                    VALUES (%s, %s)"""
    for genre_id in movie.get('genre_ids'):
        cursor.execute(genre_query, (movie["id"], genre_id))
        db.commit()

def populate_movies():
    total_pages = 1
    page = 1
    max_pages = 50 # limit to 1000 movies

    while page <= total_pages and page <= max_pages:
        print(f"Fetching page {page} of {max_pages}...")
        data = fetch_movies(page)
        if not data:
            break
        for movie in data["results"]:
            insert_movie(movie)
        page += 1
    print("Done populating movies.")

'''
Genre Handling
'''

def fetch_genres():
    url = BASE_URL + 'genre/movie/list'
    params = {
        'api_key': API_KEY,
        'language': LANG
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["genres"]
    else:
        print("Error: Failed to fetch genres: " + str(response.status_code))
        return None

def insert_genre(genre):
    query = """INSERT INTO genre (genre_id, genre_name)
            VALUES (%s, %s)"""
    values = (genre['id'], genre['name'])
    cursor.execute(query, values)
    db.commit()

def populate_genres():
    genres = fetch_genres()
    if genres:
        for genre in genres:
            insert_genre(genre["id"], genre["name"])

'''
Movie Cast Handling
'''

def fetch_movie_cast(movie_id):
    url = BASE_URL + f'/movie/{movie_id}/credits'
    params = {
        'api_key': API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Failed to fetch cast for movie {movie_id}: " + str(response.status_code)) 
        return None


def insert_movie_cast(movie_id, cast):
    query = """INSERT INTO movie_cast (movie_id, actor_id)
            VALUES (%s, %s)"""
    values =  [(movie_id, actor['id']) for actor in cast[:5]]
    cursor.execute(query, values)


def main():
    populate_movies()
    populate_genres()

if __name__ == '__main__':
    main()
