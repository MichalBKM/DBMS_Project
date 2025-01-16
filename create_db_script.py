import mysql.connector

db = mysql.connector.connect(
    host="127.0.0.1",
    port=3305,
    user="berkheim1",
    password="berkheim5501"
)

cursor = db.cursor()
cursor.execute("CREATE DATABASE mydatabase")

# movie: title, release_year, runtime, overview, popularity, votes_average, votes_count
# CREATE FULLTEXT INDEX movie_title_index ON movie(title) AFTER table is created!
cursor.execute("""CREATE TABLE movie (
                 movie_id INT AUTO_INCREMENT PRIMARY KEY,
                 title VARCHAR(255) NOT NULL,
                 release_year INT NOT NULL,
                 runtime INT NOT NULL,
                 overview TEXT NOT NULL,
                 popularity FLOAT,
                 votes_average FLOAT,
                 votes_count INT
                 FULLTEXT (title)
)""")

# genre
cursor.execute("""CREATE TABLE genre (
                 genre_id INT AUTO_INCREMENT PRIMARY KEY,
                 genre_name VARCHAR(255) NOT NULL
)""")

# movie genre: many to many relationship - there can be multiple genres for a movie
cursor.execute("""CREATE TABLE movie_genre (
                 movie_id INT,
                 genre_id INT,
                 PRIMARY KEY (movie_id, genre_id),
                 FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE,
                 FOREIGN KEY (genre_id) REFERENCES genre(genre_id) ON DELETE CASCADE
)""")

# actor: actor_id, actor_name, birth_date
cursor.execute("""CREATE TABLE actor (
                 actor_id INT AUTO_INCREMENT PRIMARY KEY,
                 actor_name VARCHAR(255) NOT NULL,
                 birth_date DATE NOT NULL
)""")


# movie cast: many to many relationship - data about the actors in a movie
cursor.execute("""CREATE TABLE movie_cast (
                 movie_id INT,
                 actor_id INT,
                 PRIMARY KEY (movie_id, actor_id),
                 FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE,
                 FOREIGN KEY (actor_id) REFERENCES actor(actor_id) ON DELETE CASCADE
)""")


# director: director_id, director_name, birth_date
cursor.execute("""CREATE TABLE director (
                 director_id INT AUTO_INCREMENT PRIMARY KEY,
                 director_name VARCHAR(255) NOT NULL,
                 birth_date DATE NOT NULL
)""")

# movie director: many to many relationship - data about the directors of a movie
cursor.execute("""CREATE TABLE movie_director (
                 movie_id INT,
                 director_id INT,
                 PRIMARY KEY (movie_id, director_id),
                 FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE,
                 FOREIGN KEY (director_id) REFERENCES director(director_id) ON DELETE CASCADE
)""") 

# keyword: keyword_id, keyword_name
cursor.execute("""CREATE TABLE keyword (
                 keyword_id INT PRIMARY KEY,
                 keyword_name VARCHAR(255) UNIQUE NOT NULL
)""")

# movie keyword: many to many relationship - data about the keywords of a movie
cursor.execute("""CREATE TABLE movie_keyword (
                 movie_id INT,
                 keyword_id INT,
                 PRIMARY KEY (movie_id, keyword_id),
                 FOREIGN KEY (movie_id) REFERENCES movie(movie_id) ON DELETE CASCADE,
                 FOREIGN KEY (keyword_id) REFERENCES keyword(keyword_id) ON DELETE CASCADE
)""")