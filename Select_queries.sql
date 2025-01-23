-- DELETE FROM genre WHERE genre_id > 0
-- SELECT * FROM genre
-- select * from keyword
-- select * from movie
-- select * from person
-- SELECT * FROM movie WHERE MATCH(title, overview) AGAINST("Modern")

-- SELECT movie.title, movie.release_year 
-- FROM movie, person, movie_person
-- WHERE person.person_name LIKE 'Tom Hanks'
-- AND movie.movie_id = movie_person.movie_id
-- AND movie_person.person_id = person.person_id


SELECT genre.genre_name 
FROM genre, movie_genre, movie
WHERE movie.title LIKE 'Forrest Gump'
AND movie.movie_id = movie_genre.movie_id
AND movie_genre.genre_id = genre.genre_id