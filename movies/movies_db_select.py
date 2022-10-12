import pandas as pd
import sqlite3
from movies.imdb import add_new_movie
import sys

movies_db = 'data/movies.db'


def create_connection(db_file):
    return sqlite3.connect(db_file)


def select_movie_by_title(title):
    conn = sqlite3.connect(movies_db)
    cur = conn.cursor()
    query = cur.execute("SELECT * FROM movie WHERE Title=?", (title,))

    rows = query.fetchall()

    if len(rows) < 1:
        try:
            print("["+title+"]: No results in database. Adding entry.")
            add_new_movie(title, movies_db)
            print("["+title+"]: Movie added.")
        except:
            print("["+title+"]: Error when adding the movie: " + str(sys.exc_info()[0]))


    df = pd.read_sql_query("SELECT * FROM movie WHERE Title==\'" + title + "\'", conn)
    return df
