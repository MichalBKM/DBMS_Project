import mysql.connector

db = mysql.connector.connect(
    host="127.0.0.1",
    port=3305,
    user="berkheim1",
    password="berkheim5501"
)
# To connect to the database, follow the following steps:
# 1. Global protect (bring your phone nearby) 
# 2. Run the following command in your terminal to create an SSH tunnel:
# ssh -L 3305:mysqlsrv1.cs.tau.ac.il:3306 berkheim1@nova.cs.tau.ac.il
# and enter your password
# 3. write in the nova the following command (and open mysql-workbench in the meantime):
# mysql-workbench
# 4. you can open MySQL-Workbench for debugging and running simple queries
# you are ready!

cursor = db.cursor()
cursor.execute("USE berkheim1")

def index_exists(table_name, index_name):
    cursor.execute(f"""
        SELECT COUNT(*)
        FROM information_schema.statistics
        WHERE table_schema = DATABASE()
          AND table_name = '{table_name}'
          AND index_name = '{index_name}';
    """)
    return cursor.fetchone()[0] > 0

def create_tables():
    # genre: genre_id, genre_name
    cursor.execute("""CREATE TABLE IF NOT EXISTS genre (
                    genre_id INT PRIMARY KEY,
                    genre_name VARCHAR(255) NOT NULL
                    )""")

    print("✅ Done creating genre table")


    # person: person_id, person_name, birthday
    cursor.execute("""CREATE TABLE IF NOT EXISTS person (
                    person_id INT NOT NULL,
                    person_name VARCHAR(255) NOT NULL,
                    birthday DATE NOT NULL,
                    PRIMARY KEY (person_id)
                    )""")

    print("\n✅ Done creating person table")

    # director: director_id (is-a person)
    cursor.execute("""CREATE TABLE IF NOT EXISTS director (
                    director_id INT NOT NULL,
                    PRIMARY KEY (director_id),
                    FOREIGN KEY (director_id) REFERENCES person(person_id)
                    )""")

    print("\n✅ Done creating director table")

    # actor: actor_id (is-a person)
    cursor.execute("""CREATE TABLE IF NOT EXISTS actor (
                    actor_id INT NOT NULL,
                    PRIMARY KEY (actor_id),
                    FOREIGN KEY (actor_id) REFERENCES person(person_id)
                    )""")

    print("\n✅ Done creating actor table")

    # movie: movie_id, title, director_id, release_year, runtime, overview, popularity, votes_average, votes_count
    # (one to many relationship - director_id is a foreign key to director_id - each movie has one director)
    cursor.execute("""CREATE TABLE IF NOT EXISTS movie (
                    movie_id INT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    director_id INT NOT NULL,
                    release_year INT NOT NULL,
                    runtime INT NOT NULL,
                    overview TEXT NOT NULL,
                    popularity FLOAT,
                    vote_average FLOAT,
                    vote_count INT,
                    FOREIGN KEY (director_id) REFERENCES director(director_id)
                    )""")

    # Altering movie table to support fulltext index
    cursor.execute("""ALTER TABLE movie ADD FULLTEXT(title, overview)""")

    # Create index to support filtering movies by year
    if not index_exists("movie", "idx_release_year"):
        cursor.execute("""CREATE INDEX idx_release_year ON movie(release_year)""")

    # Create index to support filtering movies by popularity
    if not index_exists("movie", "idx_popularity"):
        cursor.execute("""CREATE INDEX idx_popularity ON movie(popularity)""")

    # Create index to support filtering movies by vote average
    if not index_exists("movie", "idx_vote_average"):
        cursor.execute("""CREATE INDEX idx_vote_average ON movie(vote_average)""")

    print("\n✅ Done creating movie table")

    # novie_genre: movie_id, genre_id
    # (many to many relationship - there can be multiple genres for a movie)
    cursor.execute("""CREATE TABLE IF NOT EXISTS movie_genre (
                    movie_id INT,
                    genre_id INT,
                    PRIMARY KEY (movie_id, genre_id),
                    FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
                    FOREIGN KEY (genre_id) REFERENCES genre(genre_id)
                    )""")

    print("\n✅ Done creating movie-genre table")

    # movie_actor: movie_id, actor_id
    # (many to many relationship - data about the actors in a movie)
    cursor.execute("""CREATE TABLE IF NOT EXISTS movie_actor (
                    movie_id INT,
                    actor_id INT,
                    PRIMARY KEY (movie_id, actor_id),
                    FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
                    FOREIGN KEY (actor_id) REFERENCES actor(actor_id)
                    )""")

    print("\n✅ Done creating movie_actor table")

    # keyword: keyword_id, keyword_name
    cursor.execute("""CREATE TABLE IF NOT EXISTS keyword (
                    keyword_id INT PRIMARY KEY,
                    keyword_name VARCHAR(255) UNIQUE NOT NULL
    )""")

    # Altering keyword table to support fulltext index
    cursor.execute("""ALTER TABLE keyword ADD FULLTEXT(keyword_name)""")

    print("\n✅ Done creating keyword table")

    # movie_keyword: movie_id, keyword_id
    # (many to many relationship - data about the keywords of a movie)
    cursor.execute("""CREATE TABLE IF NOT EXISTS movie_keyword (
                    movie_id INT,
                    keyword_id INT,
                    PRIMARY KEY (movie_id, keyword_id),
                    FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
                    FOREIGN KEY (keyword_id) REFERENCES keyword(keyword_id)
    )""")

    print("\n✅ Done creating movie-keyword table")

    db.commit()

    print("====================================\n")
    print("🚀 Done creating database successfully!\n")

if __name__ == '__main__':
    create_tables()
