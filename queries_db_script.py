'''
import
'''
from create_db_script import cursor

#1 FULL-TEXT - Search words that appear in a movie title or overview
#              output the title of the movie, its genre, overview, rating
def query_1():
    print("""You can find the movie you want even if you don't remember the title, 
          just enter a single word that appears in the title or overview!\n""")
    input_1 = input("Enter words to search in movie the title \ overview (e.g., 'modern'):  ")
    query_1_text = """SELECT DISTINCT m.title, 
                        GROUP_CONCAT(g.genre_name ORDER BY g.genre_name SEPARATOR ', ') AS genres, 
                        m.release_year, 
                        m.overview, 
                        m.vote_average
                    FROM movie m
                    JOIN movie_genre m_g ON m.movie_id = m_g.movie_id
                    JOIN genre g ON m_g.genre_id = g.genre_id
                    WHERE MATCH(m.title, m.overview) AGAINST(%s)
                    GROUP BY m.movie_id
                    ORDER BY m.release_year DESC, m.vote_average DESC;
    """
    cursor.execute(query_1_text, (input_1,))
    return cursor.fetchall()


# without group_concat - will return multiple rows for each movie
"""
SELECT m.title, g.genre_name, m.release_year, m.overview, m.vote_average
                    FROM movie m
                    JOIN movie_genre m_g ON m.movie_id = m_g.movie_id
                    JOIN genre g ON m_g.genre_id = g.genre_id
                    WHERE MATCH(title, overview) AGAINST(%s)
                    ORDER BY m.release_year DESC, m.vote_average DESC;
"""

#2 FULL-TEXT - Search keywords that are related to movies
#              output the title of the movie, its overview, rating, release year and director
def query_2():
    print("You can find movies that are related to a specific keyword, just enter the keyword!\n")
    input_2 = input("Enter a single keyword to see what movies are related to it (e.g., 'silent'):  ")
    query_2_text = """SELECT DISTINCT m.title, m.release_year, p.person_name AS director, m.overview, m.vote_average
                 FROM movie m
                 JOIN movie_keyword m_k ON m.movie_id = m_k.movie_id
                 JOIN keyword k ON m_k.keyword_id = k.keyword_id
                 JOIN person p ON m.director_id = p.person_id
                 WHERE MATCH(k.keyword_name) AGAINST(%s)
                 ORDER BY m.release_year DESC, m.vote_average DESC;
                """
    cursor.execute(query_2_text, (input_2,))
    return cursor.fetchall()

#3 COMPLEX QUERY: "Director's favourite actors" - which actors have appeared in the 10 most popular movies of a given director
#                 and how many times have they appeared?
def query_3():
    print("Find the actors who appeared in the 10 most popular movies of your favourite director and how many times they appeared!\n")
    input_3 = input("Enter a director's name (e.g, 'John Lasseter'):    ")
    query_3_text = """SELECT p.person_name AS name, COUNT(m_a.actor_id) AS movie_count, p.person_id
                    FROM (
                            SELECT m.movie_id
                            FROM movie m
                            JOIN person p1 ON m.director_id = p1.person_id
                            AND p1.person_name = %s
                            ORDER BY m.popularity DESC
                            LIMIT 10
                    ) AS top_movies
                    JOIN movie m ON m.movie_id = top_movies.movie_id
                    JOIN movie_actor m_a ON m.movie_id = m_a.movie_id
                    JOIN actor a ON m_a.actor_id = a.actor_id
                    JOIN person p ON a.actor_id = p.person_id
                    GROUP BY p.person_name, p.person_id
                    ORDER BY movie_count DESC
                    LIMIT 20;
                    """
  
    cursor.execute(query_3_text, (input_3,))
    return cursor.fetchall()
 
#4 COMPLEX QUERY: "Hall of Fame" - for a given decade and sub-genre, 
# output the first 10 actors who played in the most movies of that sub-genre in that decade
def query_4():
    print("""we will now present the hall of fame for a sub-genre in a given decade - meaning the actors who played in the most movies of that sub-genre in that decade\n""")
    decade_start = input("""Enter a decade see the hall of fame for a sub-genre in that decade (e.g, '1960' will mean the sixties [1960-1969 both included]):   """)
    sub_genre = input("Now enter the sub-genre you want to check! (e.g, 'drama'):   ")
    decade_start = int(decade_start)
    decade_end = decade_start + 9
    query_4_text = """SELECT p.person_name AS name, p.person_id, p.birthday, COUNT(m.movie_id) as movie_count
                FROM movie m, person p, movie_actor m_a, movie_genre m_g, genre g, actor a
                WHERE m.release_year <= %s
                AND m.release_year >= %s
                AND m.movie_id = m_a.movie_id
                AND m_a.actor_id = a.actor_id
                AND a.actor_id = p.person_id
                AND m.movie_id = m_g.movie_id
                AND m_g.genre_id = g.genre_id
                AND g.genre_name = %s
                GROUP BY p.person_name, p.person_id 
                ORDER BY movie_count DESC
                LIMIT 10;
    """
    values = (str(decade_end), str(decade_start), sub_genre)
    cursor.execute(query_4_text, values)
    return cursor.fetchall()

#5 COMPLEX QUERY: "Hidden Gems" - unpopular but highly rated movies for a given year (rating > 7.0 and popularity < average popularity)
# find your next movie reccomendation!
def query_5():
    print("We will now present the hidden gems for a given year  - meaning the unpopular but highly rated movies for a given year\n")
    input_5 = input("Enter a specific year to get the hidden gems from that year! (e.g, '2001'):    ")
    query_5_text = """SELECT m.title, m.overview, m.vote_average, m.popularity
                        FROM movie m
                        WHERE m.vote_average > 7.0
                        AND m.release_year = %s
                        AND m.popularity < (
                            SELECT AVG(popularity) FROM movie
                        )
                     ORDER BY m.vote_average DESC;
    """
    cursor.execute(query_5_text, (input_5,))
    return cursor.fetchall()

###################
#  EXTRA QUERIES  #
###################
#6 EXTRA QUERY: "Most popular movies of a director" - for a given director, output their 5 most popular movies
def query_6():
    print("We will now present the most popular movies for a given director\n")
    input_6 = input("Enter your favourite director's name to see their most popular movies! (e.g, 'Woody Allen'):   ")
    query_6_text = """SELECT m.title, m.overview, m.release_year, m.popularity
                        FROM movie m
                        JOIN person p ON m.director_id = p.person_id
                        WHERE p.person_name = %s
                        ORDER BY m.popularity DESC
                        LIMIT 5;
    """
    cursor.execute(query_6_text, (input_6,))
    return cursor.fetchall()

#7 EXTRA QUERY: "Most popular movies of an actor" - for a given actor, output their 5 most popular movies
def query_7():
    print("We will now present the most popular movies for a given actor\n")
    input_7 = input("Enter your favourite actor's name to see the next movie you need to see! (e.g, 'Tom Hanks'):   ")
    query_7_text = """SELECT m.title, m.overview, m.release_year, m.popularity
                        FROM movie m
                        JOIN movie_actor m_a ON m.movie_id = m_a.movie_id
                        JOIN person p ON m_a.actor_id = p.person_id
                        WHERE p.person_name = %s
                        ORDER BY m.popularity DESC
                        LIMIT 5;
    """
    cursor.execute(query_7_text, (input_7,))
    return cursor.fetchall()

#8 EXTRA QUERY: "Most popular genres of an actor" - for a given actor, output the genres they have appeared in the most
def query_8():
    print("We will now present the genres a given actor has appeared in the most\n")
    input_8 = input("Enter an actor's name to see the genres they have appeared in the most (e.g, 'Meryl Streep'):  ")
    query_8_text = """SELECT g.genre_name, COUNT(m.movie_id) as movie_count
                        FROM movie m
                        JOIN movie_actor m_a ON m.movie_id = m_a.movie_id
                        JOIN actor a ON m_a.actor_id = a.actor_id
                        JOIN movie_genre m_g ON m.movie_id = m_g.movie_id
                        JOIN genre g ON m_g.genre_id = g.genre_id
                        JOIN person p ON a.actor_id = p.person_id
                        WHERE p.person_name = %s
                        GROUP BY g.genre_name
                        ORDER BY movie_count DESC;
    """
    cursor.execute(query_8_text, (input_8,))
    return cursor.fetchall()
