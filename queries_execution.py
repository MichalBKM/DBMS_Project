'''
import
'''
import pandas as pd
from queries_db_script import *

############################
#      HELPER FUNCTION     #
############################
def resultsToDF(results, columns):
    if results:
        df = pd.DataFrame(results, columns=columns)
        return df
    else:
        return None

def main():
    num = int(input("what query do you wish to use?     "))
    ####################
    #      QUERY 1     #
    ####################
    if num == 1:
        results = query_1()
        df = resultsToDF(results, ["title", "genres", "release year", "overview", "vote average"])
        if df is not None:
            print(df)

    ####################
    #      QUERY 2     #
    ####################
    elif num == 2:
        results = query_2()
        df = resultsToDF(results, ["title", "release year", "director", "overview", "vote average"])
        if df is not None:
            print(df)
        else:
            print("No results found")
   
    ####################
    #      QUERY 3     #
    ####################
    elif num == 3:
        results = query_3()
        df = resultsToDF(results, ["name", "movie count", "id"])[["name", "movie count"]]
        if df is not None:
            print(df)
        else:
            print("No results found")
    
    ####################
    #      QUERY 4     #
    ####################
    elif num == 4:
        results = query_4()
        df = resultsToDF(results, ["movie count", "name", "id", "birthday"])[["movie count", "name", "birthday"]]
        if df is not None:
            print(df)
        else:
            print("No results found")
        
    ####################
    #      QUERY 5     #
    ####################
    elif num == 5:
        results = query_5()
        df = resultsToDF(results, ["title", "release year", "overview", "rating", "popularity"])
        if df is not None:
            print(df)
        else:
            print("No results found")

    ####################
    #      QUERY 6     #
    ####################
    elif num == 6:
        results = query_6()
        df = resultsToDF(results, ["title", "overview", "release year", "popularity"])
        if df is not None:
            print(df)
        else:
            print("No results found")

    ####################
    #      QUERY 7     #
    ####################
    elif num == 7:
        results = query_7()
        df = resultsToDF(results, ["title", "overview", "release year", "popularity"])
        if df is not None:
            print(df)
        else:
            print("No results found")
    
    ####################
    #      QUERY 8     #
    ####################
    elif num == 8:
        results = query_8()
        df = resultsToDF(results, ["genre name", "movie count"])
        if df is not None:
            print(df)
        else:
            print("No results found")

if __name__ == '__main__':
    main()