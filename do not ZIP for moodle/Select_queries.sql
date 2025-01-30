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

SELECT keyword.keyword_name FROM movie, keyword, movie_keyword
WHERE movie.movie_id = movie_keyword.movie_id
AND movie_keyword.keyword_id = keyword.keyword_id
AND movie.title = "To All the Boys: P.S. I Still Love You"