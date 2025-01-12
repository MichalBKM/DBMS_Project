import requests
import json

# OUR DBMS PROJECT: best 1000 comedy movies of all times (full-length, English, US)

API_KEY = '82cd47774ed6c624ce7b0e24a89048c3'  # your API key from TMDB website
BASE_URL = 'https://api.themoviedb.org/3/discover/movie'
CREDITS_URL = 'https://api.themoviedb.org/3/movie/{movie_id}/credits'
OUTPUT_FILE = 'movies.json'
GENRE_ID = 35  # Genre ID for comedy movies
LANG = 'en'
REGION = 'US'

def get_movies(page):
    params = {
        'api_key': API_KEY,  # Add API key for authentication
        'with_genres': GENRE_ID,  # Filter only comedy movies
        'language': LANG,  # Filter only English movies from US
        'with_original_language': LANG,  # Filter only English movies from US
        'with_runtime.gte': 70,  # Filter only full-length movies
        'region': REGION,  # Filter only movies released in US
        'sort_by': 'vote_average.desc',  # Sort by highest user rating
        'vote_count.gte': 500,  # Filter only movies with at least 100 votes
        'page': page,
    }

    response = requests.get(BASE_URL, params=params)  # Make the request with correct URL and params
    if response.status_code == 200:
        data = response.json()
        if page == 1:
            print(f"Found {data['total_results']} Movies")
        return data
    else:
        print("Error: Failed to fetch data: " + str(response.status_code))
        return None

def save_to_file(data):
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f)

'''
def get_credits(movie_id):
    url = CREDITS_URL.format(movie_id=movie_id)
    params = {'api_key': API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        credits = response.json()
        # Filter the first 5 main actors
        cast = credits.get('cast', [])[:5]
        # Filter only the director from the crew
        crew = [member for member in credits.get('crew', []) if member.get('job') == 'Director']
        return {'cast': cast, 'director': crew}
    else:
        print(f"Error fetching credits for movie {movie_id}: {response.status_code}")
        return {'cast': [], 'director': []}
'''

def main():
    all_movies = []
    total_pages = 1
    page = 1
    max_pages = 50 # limit to 1000 movies

    while page <= total_pages and page <= max_pages:
        print(f"Fetching page {page} of {max_pages}...")
        data = get_movies(page)
        if data:
            all_movies.extend(data['results'])
            total_pages = data['total_pages']
            '''
            if total_pages > 500:
                print(f"Warning: Too many pages ({total_pages}), max 500 pages, exiting...")
                return None
            
            for movie in data['results']:
                movie_id = movie['id']
                credits = get_credits(movie_id)
                if credits:
                    movie['cast'] = credits.get('cast', [])
                    movie['crew'] = credits.get('crew', [])
                all_movies.append(movie)
            '''
        else:
            break  
        page += 1

    print(f"Fetched {len(all_movies)} movies, saving to file!...") 
    save_to_file(all_movies)
    print(f"Done saving to file {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
