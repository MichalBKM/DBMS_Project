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

# hidden gems, sub-genres, actors, years - we can output not only strings but numbers :)
# COMPLEX QUERY #3: "hidden gems"
# COMPLEX QUERY #4  "by year"
# COMPLEX QUERY #5 "directors' popular movies"

#1 FULL-TEXT - Search words that appear in the movie title or overview
# what details we want to return except title\overview
def query_1():
    input_1 = input("Enter words to search in movie titles\overview (e.g., 'Modern'): ")
    query_1_text = "SELECT title, overview FROM movie WHERE MATCH(title, overview) AGAINST(%s)"
    cursor.execute(query_1_text, (input_1,))
    return cursor.fetchall()

#2 FULL-TEXT - Search keywords that are related to movies
# what details we want to return except title
def query_2():
    input_2 = input("Enter keyword to see in what movies it appears in (e.g., 'silent film'): ")
    query_2_text = """SELECT m.title 
                 FROM movie m, keyword k, movie_keyword m_k 
                 WHERE   m_k.movie_id = m.movie_id       AND
                         m_k.keyword_id = k.keyword_id   AND
                         MATCH(k.keyword_name) AGAINST(%s)
                """
    cursor.execute(query_2_text, (input_2,))
    return cursor.fetchall()

#3 COMPLEX QUERY - Highest rated movie for a given director
# CHECK: how to solve duplicates (distinct??)
# what details we want to return except title
def query_3():
    input_3 = input("Enter director's name to see their highest rated movie (e.g., 'Steven Spielberg'): ")
    query_3_text = """ SELECT DISTINCT m.title 
                FROM movie m
                JOIN movie_person m_p ON m.movie_id = m_p.movie_id
                JOIN person p ON m_p.person_id = p.person_id
                WHERE p.role = 'Directing'
                AND p.person_name LIKE %s
                AND m.vote_average = (
                    SELECT MAX(m2.vote_average)
                    FROM movie m2
                    JOIN movie_person m_p2 ON m2.movie_id = m_p2.movie_id
                    JOIN person p2 ON m_p2.person_id = p2.person_id
                    WHERE p2.role = 'Directing'
                        AND p2.person_name LIKE %s
                    )"""
    cursor.execute(query_3_text, (f"%{input_3}%",f"%{input_3}%"))
    return cursor.fetchall()

#4 COMPLEX QUERY: For each actor in a specific year, in how many movie per genre he participated (group by)
'''note that the sum of all the counts of an actor should !not! be equal to the total number of movies he participated in,
because each movie can have multiple genres'''
def query_4():
    input_4 = input("Enter a specific year to see how many movies per genre each actor participated in (e.g., '1999'): ")
    query_4_text = """SELECT COUNT(m.movie_id) as movie_count, g.genre_name, p.person_name
                FROM movie m, person p, movie_person m_p, movie_genre m_g, genre g
                WHERE m.release_year = %s
                AND m.movie_id = m_p.movie_id
                AND m_p.person_id = p.person_id
                AND m.movie_id = m_g.movie_id
                AND m_g.genre_id in (SELECT genre_id FROM genre
                                    WHERE genre_id = m_g.genre_id 
                                    )
                GROUP BY p.person_name, g.genre_name 
    """
    cursor.execute(query_4_text, (input_4,))
    return cursor.fetchall()



def main():
    # Prompt the user for search keywords
    #input_1 = input("Enter keywords to search for movies (e.g., 'funny comedy'): ")
    # Execute the query
    #print(f"\nSearching for movies with these words: '{input_1}'...\n")
    #results = query_1(input_1)
    """
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
    """

    """
    results = query_3()
    # Display the results
    if results:
        print(f"Found {len(results)} movies matching your search:\n")
        for movie in results:
            title = movie[0]
            print(f"Title: {title}")
            print("-" * 50)  # Separator between movies
    else:
        print("No movies found matching your search.")
    """
    results = query_4()
    # Display the results
    if results:
        print(f"Found {len(results)} movies matching your search in the specified year:\n")
        for movie in results:
            movie_count, genre_name, person_name = movie
            print(f"actor: {person_name}")
            print(f"genre_name: {genre_name}")
            print(f"count: {movie_count}")
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