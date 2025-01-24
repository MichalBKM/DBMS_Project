'''
import
'''
from create_db_script import cursor

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

"""""
WITH RankedMovies AS (
    SELECT
        title,
        director,
        rating,
        ROW_NUMBER() OVER (PARTITION BY director ORDER BY rating DESC) AS rank
    FROM
        movies
)
SELECT
    title,
    director,
    rating
FROM
    RankedMovies
WHERE
    rank <= 3
ORDER BY
    director,
    rank;
"""


#3 COMPLEX QUERY - 3 highest rated movies for a given director
# CHECK: how to solve duplicates (distinct??)
# what details we want to return except title
def query_3():
    input_3 = input("Enter director's name to see their highest rated movie (e.g., 'Steven Spielberg'): ")
    if False:
        query_3_text = """" SELECT m.title 
                        FROM movie m, person p, director d
                        WHERE p.person_name LIKE %s
                        AND p.person_id = d.director_id
                        AND d.director_id = m.director_id
                        AND m.vote_average = (
                            SELECT MAX(m2.vote_average)
                            FROM movie m2, director d2, person p2
                            WHERE p2.person_name LIKE %s
                            AND p2.person_id = d2.director_id
                            AND d2.director_id = m2.director_id
                            )
                """
    else:
        query_3_text = """
    SELECT m.title
    FROM movie m
    JOIN person p ON m.director_id = p.person_id
    JOIN director d ON p.person_id = d.director_id
    WHERE p.person_name LIKE %s
    AND m.vote_average = (
                        SELECT MAX(m2.vote_average)
                        FROM movie m2
                        JOIN person p2 ON m2.director_id = p2.person_id
                        JOIN director d2 ON p2.person_id = d2.director_id
                        WHERE p.person_name LIKE %s
                        )
    """
    cursor.execute(query_3_text, (f"%{input_3}%",f"%{input_3}%"))
    return cursor.fetchall()
"""WITH movies_rated_by_director AS (
                    SELECT movie_id , director_id, vote_average, ROW_NUMBER() OVER (PARTITION BY director_id ORDER BY vote_average DESC) AS rank
                    FROM movies
                    )
                    SELECT title
                    FROM movies_rated_by_director mrbd, director d, person p, movie m    
                    WHERE mrbd.rank <= 3 AND
                    p.person_name LIKE %s AND
                    p.person_id = d.director_id AND
                    d.director_id = m.director_id AND
                    m.movie_id = mrbd.movie_id
                    """


#TODO: the query for a range of years!
#4 COMPLEX QUERY: For each actor in a specific year (maybe for a specific decade - 1960s), in how many movie per genre he participated (group by)
'''note that the sum of all the counts of an actor should !not! be equal to the total number of movies he participated in,
because each movie can have multiple genres'''
def query_4():
    #TODO: fix query_4
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

#TODO: query_5
def query_5():
    input_5 = input("Enter a specific year to see how many movies per genre each actor participated in (e.g., '1999'): ")
    query_5_text = """SELECT COUNT(m.movie_id) as movie_count, g.genre_name, p.person_name
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
    cursor.execute(query_5_text, (input_5,))
    return cursor.fetchall()



