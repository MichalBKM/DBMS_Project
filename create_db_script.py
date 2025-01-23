import mysql.connector

db = mysql.connector.connect(
    host="127.0.0.1",
    port=3305,
    user="berkheim1",
    password="berkheim5501"
)

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

# movie: title, release_year, runtime, overview, popularity, votes_average, votes_count
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

# genre
cursor.execute("""CREATE TABLE IF NOT EXISTS genre (
                 genre_id INT PRIMARY KEY,
                 genre_name VARCHAR(255) NOT NULL
)""")

print("✅ Done creating genre table")

# movie genre: many to many relationship - there can be multiple genres for a movie
cursor.execute("""CREATE TABLE IF NOT EXISTS movie_genre (
                 movie_id INT,
                 genre_id INT,
                 PRIMARY KEY (movie_id, genre_id),
                 FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
                 FOREIGN KEY (genre_id) REFERENCES genre(genre_id)
)""")

print("✅ Done creating movie-genre table")

# person: person_id, person_name, birth_date
cursor.execute("""CREATE TABLE IF NOT EXISTS person (
                 person_id INT NOT NULL,
                 person_name VARCHAR(255) NOT NULL,
                 birthday DATE NOT NULL,
                 role ENUM('Acting', 'Directing') NOT NULL,
                 PRIMARY KEY (person_id, role)
)""")

print("✅ Done creating person table")

# movie person: many to many relationship - data about the actors \ crew in a movie
cursor.execute("""CREATE TABLE IF NOT EXISTS movie_person (
                 movie_id INT,
                 person_id INT,
                 role ENUM('Acting', 'Directing') NOT NULL,
                 PRIMARY KEY (movie_id, person_id, role),
                 FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
                 FOREIGN KEY (person_id) REFERENCES person(person_id)
)""")

# Create index to support filtering/searching actors or directors by name
if not index_exists("person", "idx_role_name"):
    cursor.execute("""CREATE INDEX idx_role_name ON person(role, person_name)""")

print("✅ Done creating movie-person table")

# keyword: keyword_id, keyword_name
cursor.execute("""CREATE TABLE IF NOT EXISTS keyword (
                 keyword_id INT PRIMARY KEY,
                 keyword_name VARCHAR(255) UNIQUE NOT NULL
)""")

# Altering keyword table to support fulltext index
cursor.execute("""ALTER TABLE keyword ADD FULLTEXT(keyword_name)""")

print("✅ Done creating keyword table")

# movie keyword: many to many relationship - data about the keywords of a movie
cursor.execute("""CREATE TABLE IF NOT EXISTS movie_keyword (
                 movie_id INT,
                 keyword_id INT,
                 PRIMARY KEY (movie_id, keyword_id),
                 FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
                 FOREIGN KEY (keyword_id) REFERENCES keyword(keyword_id)
)""")

print("✅ Done creating movie-keyword table")

db.commit()

print("====================================\n")
print("🚀 Done creating database successfully!\n")
