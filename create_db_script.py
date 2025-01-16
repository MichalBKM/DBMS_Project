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
cursor.execute("""CREATE TABLE movie (
                 movie_id INT AUTO_INCREMENT PRIMARY KEY,
                 title VARCHAR(255),
                 release_year INT,
                 runtime INT,
                 overview TEXT,
                 popularity FLOAT,
                 votes_average FLOAT,
                 votes_count INT,
                 full_text(title, overview)
)""")

# movie genre: many to many relationship - there can be multiple genres for a movie
cursor.execute("""CREATE TABLE movie_genre (
                 movie_id INT,
                 genre_id INT,
                 PRIMARY KEY (movie_id, genre_id),
                 FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
                 FOREIGN KEY (genre_id) REFERENCES genre(genre_id)
)""")

# genre
cursor.execute("""CREATE TABLE genre (
                 genre_id INT AUTO_INCREMENT PRIMARY KEY,
                 genre_name VARCHAR(255)
)""")


# movie cast: many to many relationship - data about the actors in a movie
cursor.execute("""CREATE TABLE movie_cast (
                 movie_id INT,
                 actor_id INT,
                 PRIMARY KEY (movie_id, actor_id),
                 FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
                 FOREIGN KEY (actor_id) REFERENCES actor(actor_id)
)""")


# actor: actor_id, actor_name, birth_date
cursor.execute("""CREATE TABLE actor (
                 actor_id INT AUTO_INCREMENT PRIMARY KEY,
                 actor_name VARCHAR(255),
                 birth_date DATE
)""")


# director: director_id, director_name, birth_date
cursor.execute("""CREATE TABLE director (
                 director_id INT AUTO_INCREMENT PRIMARY KEY,
                 director_name VARCHAR(255),
                 birth_date DATE
)""")

# movie director: many to many relationship - data about the directors of a movie
cursor.execute("""CREATE TABLE movie_director (
                 movie_id INT,
                 director_id INT,
                 PRIMARY KEY (movie_id, director_id),
                 FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
                 FOREIGN KEY (director_id) REFERENCES director(director_id)
)""") 

