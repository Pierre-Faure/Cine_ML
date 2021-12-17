import pandas as pd
import sqlite3
from movies.imdb import add_new_movie

movies_db = 'data/movies.sqlite'


def create_connection(db_file):
    return sqlite3.connect(db_file)


def select_movie_by_title(title):
    conn = sqlite3.connect(movies_db)
    cur = conn.cursor()
    query = cur.execute("SELECT * FROM movie WHERE Title=?", (title,))

    rows = query.fetchall()

    if len(rows) == 0:
        print('No results in database. Adding entry.')
        add_new_movie(title, movies_db)
        print('Movie added.')
        select_movie_by_title(title)
    else:
        df = pd.read_sql_query("SELECT * FROM movie WHERE Title==\'"+title+"\'", conn)
        return df
