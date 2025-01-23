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

# COMPLEX QUERY #3: "hidden gems"
# COMPLEX QUERY #4  "by year"
# COMPLEX QUERY #5 "directors' popular movies"

# FULL-TEXT #1 - Search words that appear in the movie title or overview
def query_1():
    input_1 = input("Enter words to search in movie titles\overview (e.g., 'Modern'): ")
    query_1 = "SELECT title, overview FROM movie WHERE MATCH(title, overview) AGAINST(%s)"
    cursor.execute(query_1, (input_1,))
    return cursor.fetchall()

# FULL-TEXT #2 - Search keywords that are related to movies
def query_2():
    input_2 = input("Enter keyword to see in what movies it appears in (e.g., 'silent film'): ")
    query_2 = """SELECT m.title 
                 FROM movie m, keyword k, movie_keyword m_k 
                 WHERE   m_k.movie_id = m.movie_id       AND
                         m_k.keyword_id = k.keyword_id   AND
                         MATCH(k.keyword_name) AGAINST(%s)
                """
    cursor.execute(query_2, (input_2,))
    return cursor.fetchall()


def main():
    # Prompt the user for search keywords
    #input_1 = input("Enter keywords to search for movies (e.g., 'funny comedy'): ")
    # Execute the query
    #print(f"\nSearching for movies with these words: '{input_1}'...\n")
    #results = query_1(input_1)
    results = query_2()
    # Display the results
    if results:
        print(f"Found {len(results)} movies matching your search:\n")
        for movie in results:
            title = movie[0]
            print(f"Title: {title}")
            print("-" * 50)  # Separator between movies
    else:
        print("No movies found matching your search.")
    
    '''
    results = query_1()

    # Display the results
    if results:
        print(f"Found {len(results)} movies matching your search:\n")
        for movie in results:
            title, overview = movie
            print(f"Title: {title}")
            print(f"Overview: {overview}")
            print("-" * 50)  # Separator between movies
    else:
        print("No movies found matching your search.")
'''


if __name__ == '__main__':
    main()
