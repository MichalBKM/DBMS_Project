# OUR DBMS PROJECT: best 1000 comedy movies of all times (full-length, English, US)

'''
import
'''
import requests
import logging
import mysql.connector
from create_db_script import db, cursor

logging.basicConfig(level=logging.INFO)

'''
General Settings
'''
API_KEY = '82cd47774ed6c624ce7b0e24a89048c3'  # our API key from TMDB website
BASE_URL = 'https://api.themoviedb.org/3/'
LANG = 'en'
REGION = 'US'
GENRE_ID = 35  # Genre ID for comedy movies
MAX_PAGES = 50 # limits to 1000 movies - in each page there are 20 movies
               # (50 pages * 20 movies = 1000 movies)

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

'''
insering a given movie into the movie table, and its genres into the movie_genre table
'''
def insert_movie(movie, director_id):
    # insert movie into movie table
    movie_details = fetch_data(f'movie/{movie["id"]}', {})
    runtime = movie_details.get('runtime', None)
    movie_query = """INSERT INTO movie (movie_id, title, director_id, release_year, 
                    runtime, overview, popularity, vote_average, vote_count)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (
        movie["id"],
        movie.get('title', 'Unknown Title'),
        director_id,
        movie.get('release_date')[:4],
        runtime,
        movie.get('overview'),
        movie.get('popularity'),
        movie.get('vote_average'),
        movie.get('vote_count')
    )

    try:
        cursor.execute(movie_query, values)
        db.commit()
    except mysql.connector.Error as e:
        logging.error(f"❌ Error: Failed to insert movie {movie.get('title')}: {e}")
    
    # Insert genres into movie_genre table        
    genre_query =  """INSERT INTO movie_genre (movie_id, genre_id) VALUES (%s, %s)"""
    try:
        for genre_id in movie.get('genre_ids'):
            cursor.execute(genre_query, (movie["id"], genre_id))
            db.commit()
    except mysql.connector.Error as e:
        logging.error(f"❌ Error: Failed to insert genre for movie {movie.get('title')}: {e}")
    
    return movie["id"] # this return value allows us to insert rows into the 
                       # movie_actor table without fetching the movie_id again

'''
adding all the information about a movie into the database (the movie itself, its crew, and its keywords)
'''
def process_movie(movie):
    crew = populate_person(movie["id"])
    director_id = crew[0]
    movie_id = insert_movie(movie, director_id)
    for actor_id in crew[1:]:
        insert_movie_actor(movie_id, actor_id)
    populate_movie_keywords(movie["id"])
    logging.info(f"☑️  Inserted movie {movie.get('title')} into database.")

'''
TODO
'''
def populate_movies():
    total_pages = 1
    page = 1

    while page <= total_pages and page <= MAX_PAGES:
        logging.info(f"Fetching page {page} of {MAX_PAGES}...")
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
    query = """INSERT IGNORE INTO genre (genre_id, genre_name)
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
    query = f"""INSERT IGNORE INTO person (person_id, person_name, birthday)
            VALUES (%s, %s,%s)"""
    query_with_role = ""
    if role == "Directing":
        query_with_role = f"""INSERT IGNORE INTO director (director_id) VALUES (%s)"""
    elif role == "Acting":
        query_with_role = f"""INSERT IGNORE INTO actor (actor_id) VALUES (%s)"""

    endpoint = f'person/{person["id"]}'
    person_details = fetch_data(endpoint, {})
    if person_details: # if person_details is not empty
        birthday = person_details.get('birthday', None)
    else:
        logging.error(f"❌ Error: Failed to fetch person details for {person['id']}")
    values = (person['id'], person['name'], birthday)
    values_with_role = (person['id'],)
    try:
        cursor.execute(query, values)
        cursor.execute(query_with_role, values_with_role)
        db.commit()
    except mysql.connector.Error as e:
        logging.error(f"❌ Error: Failed to insert person {person['name']}: {e}")


def insert_movie_actor(movie_id, actor_id):
    query = """INSERT INTO movie_actor (movie_id, actor_id) 
            VALUES (%s, %s)"""
    values = (movie_id, actor_id)
    try:
        cursor.execute(query, values)
        db.commit()
    except mysql.connector.Error as e:
        logging.error(f"❌ Error: Failed to insert movie-actor {movie_id, actor_id}: {e}")

def populate_person(movie_id):
    credits = fetch_person(movie_id)
    has_director = False # used to look only at the main director (the first one mentioned in tmdb)
    crew = [] # the director will be the first person in the crew list, meaning crew[0] = director_id
              # the rest of the crew will be actors, indices 1-5
              # we need to return the id of the director to insert into the movie table
              # and we need to return the ids of the actors to insert into the movie_actor table
    if credits: # if credits is not empty
        for p in credits.get('crew'):
            if p['job'] == 'Director' and not has_director:
                has_director = True
                insert_person(p, "Directing")
                crew.append(p['id'])

        for p in credits.get('cast')[:5]:
            if p['known_for_department'] == 'Acting':
                insert_person(p, "Acting")
                crew.append(p['id'])
    
    return crew
##TODO: ER diagram- add not null arrow to director
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
    for keyword in keywords[:5]: #limit to the first 5 keywords for each movie - the most important
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
            logging.info(f"Total records in {table}: {count}")
        except Exception as e:
            logging.error(f"❌ Error counting records in table {table}: {e}")
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
    
    tables = ['movie', 'genre', 'movie_genre', 'person', 'movie_actor', 'keyword', 'movie_keyword', 'actor', 'director']
    cnt = count_records(cursor, tables)
    print("=================================================\n")
    print("Summary of record counts:\n")
    for table, count in cnt.items():
        print(f"{table}: {count} records")
    print("=================================================\n")
    total_recs = sum(count for count in cnt.values() if count is not None)
    print("Total number of records: ", {total_recs})


if __name__ == '__main__':
    main()
