'''
import
'''
from create_db_script import cursor


#1 FULL-TEXT - Search words that appear in the movie title or overview
# what details we want to return except title\overview
def query_1():
    print("you can find the movie you want even if you don't remember the title, \
           just enter a word that appears in the title or overview!\n")
    input_1 = input("Enter words to search in movie the title \ overview (e.g., 'Modern'): \n")
    query_1_text = "SELECT title, overview FROM movie WHERE MATCH(title, overview) AGAINST(%s);"
    cursor.execute(query_1_text, (input_1,))
    return cursor.fetchall()

#2 FULL-TEXT - Search keywords that are related to movies
# what details we want to return except title
def query_2():
    print("you can find movies that are related to a specific keyword, just enter the keyword!\n")
    input_2 = input("Enter a keyword to see what movies are related to it (e.g., 'silent film'): \n")
    query_2_text = """SELECT m.title 
                 FROM movie m, keyword k, movie_keyword m_k 
                 WHERE   m_k.movie_id = m.movie_id       AND
                         m_k.keyword_id = k.keyword_id   AND
                         MATCH(k.keyword_name) AGAINST(%s);
                """
    cursor.execute(query_2_text, (input_2,))
    return cursor.fetchall()

#3 COMPLEX QUERY - 3 highest rated movies for a given director
def query_3(): #TODO
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
        SELECT m.title, m.vote_average
        FROM movie m
        JOIN person p ON m.director_id = p.person_id
        WHERE p.person_name LIKE %s
        AND m.vote_average = (
                        SELECT MAX(m2.vote_average)
                        FROM movie m2
                        JOIN person p2 ON m2.director_id = p2.person_id
                        WHERE p2.person_name LIKE %s
                        )
        LIMIT 1;
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


#4 COMPLEX QUERY: "Hall of Fame" - for a given decade and sub-genre of comedy, 
# output the first 10 actors who played in the most movies of that sub-genre in that decade
def query_4():
    print("we will now present the hall of fame for a sub-genre in a given decade- meaning the actors who played in the most movies of that sub-genre in that decade\n")
    decade_start = input("Enter a decade see the hall of fame for a sub-genre in that decade (e.g, '1960' will mean the sixties [1960-1969 both included]):\n")
    sub_genre = input("Now enter the sub-genre you want to check! (e.g, 'horror'):\n")
    decade_start = int(decade_start)
    decade_end = decade_start + 9
    query_4_text = """SELECT COUNT(m.movie_id) as movie_count, p.person_name, p.person_id
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
                ORDER BY movie_count DESC, p.person_name ASC
                LIMIT 10;
    """
    values = (str(decade_end), str(decade_start), sub_genre)
    cursor.execute(query_4_text, values)
    return cursor.fetchall()

### find your next movie reccomendation!
#5 COMPLEX QUERY: "hidden gems" - unpopular but highly rated movies for a given year (rating > 7.0 and popularity < average popularity)
def query_5():
    print("we will now present the hidden gems for a given year- meaning the unpopular but highly rated movies for a given year\n")
    input_5 = input("Enter a specific year to get the hidden gems from that year! (e.g, '2001'): \n")
    query_5_text = """SELECT m.title, m.vote_average, m.popularity
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

#more complex queries options:
#6 COMPLEX QUERY: what actors have appeared in the 10 most popular movies of a given director and how many times they appeared?
def query_6():
    print("Find the actors who appeared in the 10 most popular movies of your favourite director and how many times they appeared!\n")
    input_6 = input("Enter a director's name (e.g, 'John Lasseter'): \n")
    query_6_text = """SELECT p.person_name, COUNT(m_a.actor_id) AS actor_count, p.person_id
                    FROM (
                            SELECT m.movie_id
                            FROM movie m, director d
                            WHERE m.director_id = d.director_id
                            AND d.director_name LIKE %s
                            ORDER BY m.popularity DESC
                            LIMIT 10
                    ) AS top_movies, movie_actor m_a, person p
                    WHERE top_movies.movie_id = m_a.movie_id
                    AND m_a.actor_id = p.person_id
                    GROUP BY p.person_name, p.person_id
                    ORDER BY actor_count DESC;
                    """
  
    cursor.execute(query_6_text, (f"%{input_6}%",))
    return cursor.fetchall()

############################################
#           copilot suggestions:           #
############################################
#6 QUERY: "directors' popular movies" - for a given director, output their most popular movies
def query_6c():
    print("we will now present the most popular movies for a given director\n")
    input_6 = input("Enter a director's name to see their most popular movies (e.g, 'Steven Spielberg'): \n")
    query_6_text = """SELECT m.title, m.popularity
                        FROM movie m
                        JOIN person p ON m.director_id = p.person_id
                        WHERE p.person_name LIKE %s
                        ORDER BY m.popularity DESC;
    """
    cursor.execute(query_6_text, (f"%{input_6}%",))
    return cursor.fetchall()

#7 QUERY: "actors' most popular movies" - for a given actor, output their most popular movies
def query_7():
    print("we will now present the most popular movies for a given actor\n")
    input_7 = input("Enter an actor's name to see their most popular movies (e.g, 'Tom Hanks'): \n")
    query_7_text = """SELECT m.title, m.popularity
                        FROM movie m
                        JOIN movie_actor m_a ON m.movie_id = m_a.movie_id
                        JOIN person p ON m_a.actor_id = p.person_id
                        WHERE p.person_name LIKE %s
                        ORDER BY m.popularity DESC;
    """
    cursor.execute(query_7_text, (f"%{input_7}%",))
    return cursor.fetchall()

#8 QUERY: "actors' highest rated movies" - for a given actor, output their highest rated movies
def query_8():
    print("we will now present the highest rated movies for a given actor\n")
    input_8 = input("Enter an actor's name to see their highest rated movies (e.g, 'Tom Hanks'): \n")
    query_8_text = """SELECT m.title, m.vote_average
                        FROM movie m
                        JOIN movie_actor m_a ON m.movie_id = m_a.movie_id
                        JOIN person p ON m_a.actor_id = p.person_id
                        WHERE p.person_name LIKE %s
                        ORDER BY m.vote_average DESC;
    """
    cursor.execute(query_8_text, (f"%{input_8}%",))
    return cursor.fetchall()

#9 COMPLEX QUERY: "actors' most popular genres" - for a given actor, output the genres they have appeared in the most
def query_9():
    print("we will now present the genres a given actor has appeared in the most\n")
    input_9 = input("Enter an actor's name to see the genres they have appeared in the most (e.g, 'Tom Hanks'): \n")
    query_9_text = """SELECT g.genre_name, COUNT(m.movie_id) as movie_count
                        FROM movie m
                        JOIN movie_actor m_a ON m.movie_id = m_a.movie_id
                        JOIN actor a ON m_a.actor_id = a.actor_id
                        JOIN movie_genre m_g ON m.movie_id = m_g.movie_id
                        JOIN genre g ON m_g.genre_id = g.genre_id
                        JOIN person p ON a.actor_id = p.person_id
                        WHERE p.person_name LIKE %s
                        GROUP BY g.genre_name
                        ORDER BY movie_count DESC;
    """
    cursor.execute(query_9_text, (f"%{input_9}%",))
    return cursor.fetchall()

#10 QUERY: "actors' highest rated genres" - for a given actor, output the genres they have appeared in the highest rated movies
def query_10():
    print("we will now present the genres a given actor has appeared in the highest rated movies\n")
    input_10 = input("Enter an actor's name to see the genres they have appeared in the highest rated movies (e.g, 'Tom Hanks'): \n")
    query_10_text = """SELECT g.genre_name, m.vote_average
                        FROM movie m
                        JOIN movie_actor m_a ON m.movie_id = m_a.movie_id
                        JOIN actor a ON m_a.actor_id = a.actor_id
                        JOIN movie_genre m_g ON m.movie_id = m_g.movie_id
                        JOIN genre g ON m_g.genre_id = g.genre_id
                        JOIN person p ON a.actor_id = p.person_id
                        WHERE p.person_name LIKE %s
                        ORDER BY m.vote_average DESC;
    """
    cursor.execute(query_10_text, (f"%{input_10}%",))
    return cursor.fetchall()

#11 COMPLEX QUERY: "actors' hidden gems" - for a given actor, output the unpopular but highly rated movies they have appeared in
def query_11():
    print("we will now present the unpopular but highly rated movies a given actor has appeared in\n")
    input_11 = input("Enter an actor's name to see the unpopular but highly rated movies they have appeared in (e.g, 'Tom Hanks'): \n")
    query_11_text = """SELECT m.title, m.vote_average, m.popularity
                        FROM movie m
                        JOIN movie_actor m_a ON m.movie_id = m_a.movie_id
                        JOIN actor a ON m_a.actor_id = a.actor_id
                        JOIN person p ON a.actor_id = p.person_id
                        WHERE p.person_name LIKE %s
                        AND m.vote_average > 7.0
                        AND m.popularity < (
                            SELECT AVG(popularity) FROM movie
                        )
                        ORDER BY m.vote_average DESC;
    """
    cursor.execute(query_11_text, (f"%{input_11}%",))
    return cursor.fetchall()

#12 QUERY: "directors' highest rated genres" - for a given director, output the genres they have directed the highest rated movies in
def query_12():
    print("we will now present the genres a given director has directed the highest rated movies in\n")
    input_12 = input("Enter a director's name to see the genres they have directed the highest rated movies in (e.g, 'Steven Spielberg'): \n")
    query_12_text = """SELECT g.genre_name, m.vote_average
                        FROM movie m
                        JOIN director d ON m.director_id = d.director_id
                        JOIN person p ON d.director_id = p.person_id
                        JOIN movie_genre m_g ON m.movie_id = m_g.movie_id
                        JOIN genre g ON m_g.genre_id = g.genre_id
                        WHERE p.person_name LIKE %s
                        ORDER BY m.vote_average DESC;
    """
    cursor.execute(query_12_text, (f"%{input_12}%",))
    return cursor.fetchall()

#13 QUERY: "directors' most popular genres" - for a given director, output the genres they have directed the most popular movies in
def query_13():
    print("we will now present the genres a given director has directed the most popular movies in\n")
    input_13 = input("Enter a director's name to see the genres they have directed the most popular movies in (e.g, 'Steven Spielberg'): \n")
    query_13_text = """SELECT g.genre_name, m.popularity
                        FROM movie m
                        JOIN director d ON m.director_id = d.director_id
                        JOIN person p ON d.director_id = p.person_id
                        JOIN movie_genre m_g ON m.movie_id = m_g.movie_id
                        JOIN genre g ON m_g.genre_id = g.genre_id
                        WHERE p.person_name LIKE %s
                        ORDER BY m.popularity DESC;
    """
    cursor.execute(query_13_text, (f"%{input_13}%",))
    return cursor.fetchall()

#14 QUERY: "directors' hidden gems" - for a given director, output the unpopular but highly rated movies they have directed
def query_14():
    print("we will now present the unpopular but highly rated movies a given director has directed\n")
    input_14 = input("Enter a director's name to see the unpopular but highly rated movies they have directed (e.g, 'Steven Spielberg'): \n")
    query_14_text = """SELECT m.title, m.vote_average, m.popularity
                        FROM movie m
                        JOIN director d ON m.director_id = d.director_id
                        JOIN person p ON d.director_id = p.person_id
                        WHERE p.person_name LIKE %s
                        AND m.vote_average > 7.0
                        AND m.popularity < (
                            SELECT AVG(popularity) FROM movie
                        )
                        ORDER BY m.vote_average DESC;
    """
    cursor.execute(query_14_text, (f"%{input_14}%",))
    return cursor.fetchall()


#15 QUERY: "actors' hidden gems genres" - for a given actor, output the genres they have appeared in the unpopular but highly rated movies
def query_15():
    print("we will now present the genres a given actor has appeared in the unpopular but highly rated movies\n")
    input_15 = input("Enter an actor's name to see the genres they have appeared in the unpopular but highly rated movies (e.g, 'Tom Hanks'): \n")
    query_15_text = """SELECT g.genre_name, m.vote_average, m.popularity
                        FROM movie m
                        JOIN movie_actor m_a ON m.movie_id = m_a.movie_id
                        JOIN actor a ON m_a.actor_id = a.actor_id
                        JOIN person p ON a.actor_id = p.person_id
                        JOIN movie_genre m_g ON m.movie_id = m_g.movie_id
                        JOIN genre g ON m_g.genre_id = g.genre_id
                        WHERE p.person_name LIKE %s
                        AND m.vote_average > 7.0
                        AND m.popularity < (
                            SELECT AVG(popularity) FROM movie
                        )
                        ORDER BY m.vote_average DESC;
    """
    cursor.execute(query_15_text, (f"%{input_15}%",))
    return cursor.fetchall()






