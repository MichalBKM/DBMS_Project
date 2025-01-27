'''
import
'''
from create_db_script import db, cursor
from queries_db_script import *

def main():
    num = int(input("what query do you wish to use?     "))
    ####################
    #      QUERY 1     #
    ####################
    if num == 1:
        results = query_1()
        # Display the results in a way that fits the query
        if results:
            print(f"\nFound {len(results)} movies matching your search:\n")
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
    elif num == 2:
        results = query_2()
        # Display the results in a way that fits the query
        if results:
            print(f"\nFound {len(results)} movies matching your search:\n")
            for movie in results:
                title = movie[0]
                print(f"Title: {title}")
                print("-" * 50)  # Separator between movies
        else:
            print("No movies found matching your search.")
   
    ####################
    #      QUERY 3     #
    ####################
    elif num == 3:
        results = query_3()
        # Display the results in a way that fits the query
        if results:
            print(f"\nFound {len(results)} movies matching your search:\n")
            for movie in results:
                title = movie[0]
                print(f"Title: {title}")
                print("-" * 50)  # Separator between movies
        else:
            print("No movies found matching your search.")
    
    ####################
    #      QUERY 4     #
    ####################
    elif num == 4:
        results = query_4()
        # Display the results in a way that fits the query
        if results:
            print(f"\nFound {len(results)} movies matching your search in the specified decade and subgenre:\n")
            for movie in results:
                movie_count, person_name = movie[0:2]
                print(f"actor: {person_name}")
                print(f"count: {movie_count}")
                print("-" * 50)  # Separator between movies
        else:
            print("No movies found matching your search.")
        
        
    ####################
    #      QUERY 5     #
    ####################
    elif num == 5:
        results = query_5()
        # Display the results in a way that fits the query
        if results:
            print(f"\nFound {len(results)} \"hidden gems\" in the specified year:\n")
            for movie in results:
                title, avg_rating, popularity = movie
                print(f"Title: {title}")
                print(f"Average rating: {avg_rating}")
                print(f"Popularity: {popularity}")
                print("-" * 50)  # Separator between movies
        else:
            print("No movies found matching your search.")



    


if __name__ == '__main__':
    main()