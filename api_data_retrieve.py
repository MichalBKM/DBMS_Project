import requests
import json

# OUR DBMS PROJECT: comedy movies (genre id = 35) from 2024

API_KEY = '82cd47774ed6c624ce7b0e24a89048c3' # my api key from TMDB website
BASE_URL = 'https://api.themoviedb.org/3/'
GENRE_ID = 35 # Comedy genre
OUTPUT_FILE = 'comedy_movies.json'
START_DATE = '2024-01-01'
END_DATE = '2024-12-31'

def get_comedy_movies(page):
    url = BASE_URL + 'discover/movie'
    params = {
        'api_key': API_KEY,
        'language': 'en-US',
        'with_genres': GENRE_ID,
        'sort_by': 'popularity.desc',
        'primary_release_date.gte': START_DATE,
        'primary_release_date.lte': END_DATE,
        'page': page,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if page == 1:
            if data['total_results'] < 5000:
                print("Found {data['total_results']}, less than 5000 records that are needed")
                return None
            print(f"Found {data['total_results']} comedy movies")
        return data
    else:
        print("Error: Failed to fetch data: " + str(response.status_code))
        return None

def save_to_file(data):
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f)

def main():
    all_movies = []
    total_pages = 1
    page = 1

    while page <= total_pages:
        print(f"Fetching page {page} of {total_pages}...")
        data = get_comedy_movies(page)
        if data:
            all_movies.extend(data['results'])
            total_pages = data['total_pages']
        else:
            break  
        page += 1

    print(f"fetched {len(all_movies)} movies, saving to file!...")
    save_to_file(all_movies)
    print(f"Done saving to file {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
