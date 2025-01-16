# OUR DBMS PROJECT: best 1000 comedy movies of all times (full-length, English, US)

'''
import
'''
import requests
import json
import logging
from create_db_script import db, cursor

logging.basicConfig(level=logging.INFO)

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
            logging.info(f"Found {data['total_results']} Movies")
        return data
    else:
        logging.info("Error: Failed to fetch data: " + str(response.status_code))
        return None

def insert_movie(movie):
    # insert movie into movie table
    movie_query = """INSERT INTO movie (title, release_year, runtime, overview, popularity, vote_average, vote_count)
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

def process_movie(movie):
    insert_movie(movie)
    logging.info("Done populating movies.")
    populate_credits(movie["id"])
    logging.info("Done populating cast and directors.")
    populate_movie_keywords(movie["id"])
    logging.info("Done populating keywords.")

def populate_movies():
    total_pages = 1
    page = 1
    max_pages = 50 # limit to 1000 movies

    while page <= total_pages and page <= max_pages:
        logging.info(f"Fetching page {page} of {max_pages}...")
        data = fetch_movies(page)
        if not data:
            break
        for movie in data["results"]:
            process_movie(movie)
        page += 1
    logging.info("Done populating tables.")

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
        logging.info("Error: Failed to fetch genres: " + str(response.status_code))
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
            insert_genre(genre)

'''
Movie Cast and Crew Handling
'''

def fetch_credits(movie_id):
    url = BASE_URL + f'movie/{movie_id}/credits'
    params = {
        'api_key': API_KEY,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        logging.info(f"Error: Failed to fetch cast for movie {movie_id}: " + str(response.status_code))
        return None


def insert_person(person, role):
    if role == "Director":
        table = "director"
    else:
        table = "actor"
    query = f"""INSERT IGNORE INTO {table} (person_id, name)
            VALUES (%s, %s)"""
    values = (person['id'], person['name'])
    cursor.execute(query, values)
    db.commit()


def insert_movie_person(movie_id, person_id, role):
    if role == "Director":
        query = """INSERT INTO movie_directors (movie_id, director_id) 
                VALUES (%s, %s)"""
    else:
        query = """INSERT INTO movie_cast (movie_id, actor_id) 
                VALUES (%s, %s)"""

    values = (movie_id, person_id)
    cursor.execute(query, values)
    db.commit()

def populate_credits(movie_id):
    credits = fetch_credits(movie_id)
    if credits:
        for person in credits.get('cast')[:5]:
            if person['known_for_department'] == 'Acting':
                insert_person(person, "Actor")
                insert_movie_person(movie_id, person['id'], "Actor")
        
        for person in credits.get('crew'):
            if person['job'] == 'Director':
                insert_person(person, "Director")
                insert_movie_person(movie_id, person['id'], "Director")

'''
Keyword handling
'''
def fetch_keywords(movie_id):
    url = BASE_URL + f'movie/{movie_id}/keywords'
    params = {
        'api_key': API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()['keywords']
    else:
        logging.info(f"Error: Failed to fetch keywords for movie {movie_id}: " + str(response.status_code))
        return None

def insert_keyword(keyword):
    try:
        query = """INSERT INTO keyword (keyword_id, keyword_name)
                VALUES (%s, %s)"""
        values = (keyword['id'], keyword['name'])
        cursor.execute(query, values)
        db.commit()
    except Exception as e:
        logging.info(f"Error: Failed to insert keyword {keyword['name']}: {e}")


def insert_movie_keyword(movie_id, keyword_id):
    query = """INSERT INTO movie_keyword (movie_id, keyword_id)
            VALUES (%s, %s)"""
    values = (movie_id, keyword_id)
    cursor.execute(query, values)
    db.commit()

def populate_movie_keywords(movie_id):
    keywords = fetch_keywords(movie_id)
    for keyword in keywords:
        insert_keyword(keyword)
        insert_movie_keyword(movie_id, keyword['id'])


def main():
    populate_movies()
    

if __name__ == '__main__':
    main()
