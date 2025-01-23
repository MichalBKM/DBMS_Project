# OUR DBMS PROJECT: best 1000 comedy movies of all times (full-length, English, US)

'''
import
'''
import os
import requests
import json
import logging
import mysql.connector
from create_db_script import db, cursor

logging.basicConfig(level=logging.INFO)

'''
General Settings
'''
API_KEY = '82cd47774ed6c624ce7b0e24a89048c3'  # your API key from TMDB website
BASE_URL = 'https://api.themoviedb.org/3/'
LANG = 'en'
REGION = 'US'
GENRE_ID = 35  # Genre ID for comedy movies


'''
Fetch helper function
'''
def fetch_data(endpoint, params):
    url = BASE_URL + endpoint
    params['api_key'] = API_KEY
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"❌ Error: Failed to fetch {endpoint}: {response.status_code}")
        return None

'''
Movie Handling
'''
def fetch_movies(page):
    return fetch_data('discover/movie', {
        'with_genres': GENRE_ID,
        'language': LANG,
        'with_original_language': LANG,
        'with_runtime.gte': 70,
        'region': REGION,
        'sort_by': 'vote_average.desc',
        'vote_count.gte': 500,
        'page': page,
    })

def insert_movie(movie):
    # insert movie into movie table
    movie_details = fetch_data(f'movie/{movie["id"]}', {})
    runtime = movie_details.get('runtime', None)
    movie_query = """INSERT INTO movie (movie_id, title, release_year, runtime, overview, popularity, vote_average, vote_count)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (
        movie["id"],
        movie.get('title', 'Unknown Title'),
        movie.get('release_date')[:4],
        runtime,
        movie.get('overview'),
        movie.get('popularity'),
        movie.get('vote_average'),
        movie.get('vote_count')
    )
    #printing values to check if the values are correct
    #print("insert_movie:" , values)
    try:
        cursor.execute(movie_query, values)
        db.commit()
    except mysql.connector.Error as e:
        logging.error(f"❌ Error: Failed to insert movie {movie.get('title')}: {e}")
    
    # Insert genres into movie_genre table
    try:
        genre_query =  """INSERT INTO movie_genre (movie_id, genre_id)
                        VALUES (%s, %s)"""
        for genre_id in movie.get('genre_ids'):
            #printing values to check if the values are correct
            #print("insert_genre:" , movie["id"], genre_id)
            cursor.execute(genre_query, (movie["id"], genre_id))
            db.commit()
    except mysql.connector.Error as e:
        logging.error(f"❌ Error: Failed to insert genre for movie {movie.get('title')}: {e}")


def process_movie(movie):
    insert_movie(movie)
    populate_person(movie["id"])
    populate_movie_keywords(movie["id"])
    logging.info(f"☑️  Inserted movie {movie.get('title')} into database.")


def populate_movies():
    total_pages = 1
    page = 1
    max_pages = 50 # limit to 1000 movies - in each page theres 20 movies

    while page <= total_pages and page <= max_pages:
        logging.info(f"Fetching page {page} of {max_pages}...")
        data = fetch_movies(page)
        if not data:
            break
        total_pages = data.get('total_pages',1)
        for movie in data["results"]:
            process_movie(movie)
        page += 1
    logging.info("✅ Done populating tables.")

'''
Genre Handling
'''
def fetch_genres():
    return fetch_data('genre/movie/list', {'language': LANG})

def insert_genre(genre):
    query = """INSERT INTO genre (genre_id, genre_name)
            VALUES (%s, %s)"""
    values = (genre['id'], genre['name'])
    try:
        cursor.execute(query, values)
        db.commit()
    except mysql.connector.Error as e:
        logging.error(f"❌ Error: Failed to insert genre {genre['name']}: {e}")

def populate_genres():
    genres = fetch_genres()
    if genres:
        for genre in genres.get('genres',[]):
            insert_genre(genre)

'''
Movie Cast and Crew Handling
'''

def fetch_person(movie_id):
    return fetch_data(f'movie/{movie_id}/credits', {})

def insert_person(person, role):
    query = f"""INSERT IGNORE INTO person (person_id, person_name, birthday, role)
            VALUES (%s, %s,%s, %s)"""
    endpoint = f'person/{person["id"]}'
    person_details = fetch_data(endpoint, {})
    if person_details:
        birthday = person_details.get('birthday', None)
    else:
        logging.error(f"❌ Error: Failed to fetch person details for {person['id']}")
    values = (person['id'], person['name'], birthday, role)
    #printing values to check if the values are correct
    #print(values)
    try:
        cursor.execute(query, values)
        db.commit()
    except mysql.connector.Error as e:
        logging.error(f"❌ Error: Failed to insert person {person['name']}: {e}")


def insert_movie_person(movie_id, person_id, role):
    query = """INSERT INTO movie_person (movie_id, person_id, role) 
            VALUES (%s, %s, %s)"""
    values = (movie_id, person_id, role)
    try:
        cursor.execute(query, values)
        db.commit()
    except mysql.connector.Error as e:
        logging.error(f"❌ Error: Failed to insert movie-person {movie_id, person_id}: {e}")

def populate_person(movie_id):
    credits = fetch_person(movie_id)
    if credits:
        for p in credits.get('cast')[:5]:
            if p['known_for_department'] == 'Acting':
                insert_person(p, "Acting")
                insert_movie_person(movie_id, p['id'], 'Acting')
        
        for p in credits.get('crew'):
            if p['job'] == 'Director':
                insert_person(p, "Directing")
                insert_movie_person(movie_id, p['id'], 'Directing')

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
        logging.info(f"❌ Error: Failed to fetch keywords for movie {movie_id}: " + str(response.status_code))
        return None

def insert_keyword(keyword):
    try:
        query = """INSERT INTO keyword (keyword_id, keyword_name)
                VALUES (%s, %s)"""
        values = (keyword['id'], keyword['name'])
        cursor.execute(query, values)
        db.commit()
    except Exception as e:
        if not ('Duplicate entry' in str(e)):
            #logging.info(f"Duplicate entry for keyword {keyword['name']}")
        #else:
            logging.error(f"❌ Error: Failed to insert keyword {keyword['name']}: {e}")

def insert_movie_keyword(movie_id, keyword_id):
    query = """INSERT INTO movie_keyword (movie_id, keyword_id)
            VALUES (%s, %s)"""
    values = (movie_id, keyword_id)
    try:
        cursor.execute(query, values)
        db.commit()
    except mysql.connector.Error as e:
        logging.error(f"❌ Error: Failed to insert movie-keyword {movie_id, keyword_id}: {e}")

def populate_movie_keywords(movie_id):
    keywords = fetch_keywords(movie_id)
    for keyword in keywords:
        insert_keyword(keyword)
        insert_movie_keyword(movie_id, keyword['id'])


def count_records(cursor, tables):
    record_counts = {}

    for table in tables:
        query = f"SELECT COUNT(*) FROM {table}"
        try:
            cursor.execute(query)
            count = cursor.fetchone()[0]
            record_counts[table] = count
            print(f"Total records in {table}: {count}")
        except Exception as e:
            print(f"❌ Error counting records in table {table}: {e}")
            record_counts[table] = None

    return record_counts


def main():
    logging.info("Populating genres...")
    populate_genres()
    logging.info("✅ Done populating genres.")
    logging.info("Populating movies...")
    populate_movies()
    print("====================================\n")
    logging.info("🚀 Database populated successfully.")
    
    tables = ['movie', 'genre', 'movie_genre', 'person', 'movie_person', 'keyword', 'movie_keyword']
    count_records = count_records(cursor, tables)
    print("=================================================\n")
    print("Summary of record counts:\n")
    for table, count in count_records.items():
        print(f"{table}: {count} records")
    print("=================================================\n")
    print("Total number of records: ", sum(count_records))


if __name__ == '__main__':
    main()
