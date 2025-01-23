import mysql.connector

db = mysql.connector.connect(
    host="127.0.0.1",
    port=3305,
    user="berkheim1",
    password="berkheim5501"
)
#
cursor = db.cursor()
cursor.execute("USE berkheim1")
#cursor.execute("CREATE DATABASE mydatabase")

# movie: title, release_year, runtime, overview, popularity, votes_average, votes_count
# CREATE FULLTEXT INDEX movie_title_index ON movie(title) AFTER table is created!
# FULLTEXT (title)
cursor.execute("""CREATE TABLE IF NOT EXISTS movie (
                 movie_id INT PRIMARY KEY,
                 title VARCHAR(255) NOT NULL,
                 release_year INT NOT NULL,
                 runtime INT NOT NULL,
                 overview TEXT NOT NULL,
                 popularity FLOAT,
                 vote_average FLOAT,
                 vote_count INT
)""")

# genre
cursor.execute("""CREATE TABLE IF NOT EXISTS genre (
                 genre_id INT PRIMARY KEY,
                 genre_name VARCHAR(255) NOT NULL
)""")

# movie genre: many to many relationship - there can be multiple genres for a movie
cursor.execute("""CREATE TABLE IF NOT EXISTS movie_genre (
                 movie_id INT,
                 genre_id INT,
                 PRIMARY KEY (movie_id, genre_id),
                 FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
                 FOREIGN KEY (genre_id) REFERENCES genre(genre_id)
)""")

# person: person_id, person_name, birth_date
cursor.execute("""CREATE TABLE IF NOT EXISTS person (
                 person_id INT NOT NULL,
                 person_name VARCHAR(255) NOT NULL,
                 birthday DATE NOT NULL,
                 role ENUM('Acting', 'Directing') NOT NULL,
                 PRIMARY KEY (person_id, role)
)""")


# movie person: many to many relationship - data about the actors \ crew in a movie
cursor.execute("""CREATE TABLE IF NOT EXISTS movie_person (
                 movie_id INT,
                 person_id INT,
                 role ENUM('Acting', 'Directing') NOT NULL,
                 PRIMARY KEY (movie_id, person_id, role),
                 FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
                 FOREIGN KEY (person_id) REFERENCES person(person_id)
)""")


# keyword: keyword_id, keyword_name
cursor.execute("""CREATE TABLE IF NOT EXISTS keyword (
                 keyword_id INT PRIMARY KEY,
                 keyword_name VARCHAR(255) UNIQUE NOT NULL
)""")

# movie keyword: many to many relationship - data about the keywords of a movie
cursor.execute("""CREATE TABLE IF NOT EXISTS movie_keyword (
                 movie_id INT,
                 keyword_id INT,
                 PRIMARY KEY (movie_id, keyword_id),
                 FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
                 FOREIGN KEY (keyword_id) REFERENCES keyword(keyword_id)
)""")
