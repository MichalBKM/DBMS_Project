'''
import
'''
from create_db_script import db, cursor
from queries_db_script import query_1, query_2, query_3, query_4


def main():
    ####################
    #      QUERY 1     #
    ####################
    
    results = query_1()
    # Display the results in a way that fits the query
    if results:
        print(f"Found {len(results)} movies matching your search:\n")
        for movie in results:
            title, overview = movie
            print(f"Title: {title}")
            print(f"Overview: {overview}")
            print("-" * 50)  # Separator between movies
    else:
        print("No movies found matching your search.")

    ####################
    #      QUERY 2     #
    ####################

    results = query_2()
    # Display the results in a way that fits the query
    if results:
        print(f"Found {len(results)} movies matching your search:\n")
        for movie in results:
            title = movie[0]
            print(f"Title: {title}")
            print("-" * 50)  # Separator between movies
    else:
        print("No movies found matching your search.")
   
    ####################
    #      QUERY 3     #
    ####################

    results = query_3()
    # Display the results in a way that fits the query
    if results:
        print(f"Found {len(results)} movies matching your search:\n")
        for movie in results:
            title = movie[0]
            print(f"Title: {title}")
            print("-" * 50)  # Separator between movies
    else:
        print("No movies found matching your search.")
    
    ####################
    #      QUERY 4     #
    ####################

    results = query_4()
    # Display the results in a way that fits the query
    if results:
        print(f"Found {len(results)} movies matching your search in the specified year:\n")
        for movie in results:
            movie_count, genre_name, person_name = movie
            print(f"actor: {person_name}")
            print(f"genre_name: {genre_name}")
            print(f"count: {movie_count}")
            print("-" * 50)  # Separator between movies
    else:
        print("No movies found matching your search.")
    
    ####################
    #      QUERY 5     #
    ####################

    


if __name__ == '__main__':
    main()