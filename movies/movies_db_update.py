import pandas as pd
from movies.imdb import add_new_movie
import sqlite3


def db_update(input_file, db_file):
    # Fetching data
    df = pd.read_csv(input_file, parse_dates=[['date', 'time']], dayfirst=True, encoding='utf-8')

    # Connecting to database
    conn = sqlite3.connect(str(db_file))
    cur = conn.cursor()

    # for movie in df['Film'].unique():
    #     # Movie exists in db ?
    #     cur.execute('SELECT Title FROM movie WHERE Title = ? ', (movie,))
    #     row = cur.fetchone()
    #
    #     if row is None:
    #         add_new_movie(movie, db_file)
    #     else:
    #         print("[" + movie + "]: Record already in base. No update made.")

    # Optimised way to fetch missing movies
    movies_in_db = list(pd.read_sql_query("SELECT * FROM movie", conn)['Title'].unique())
    movies_to_fetch = list(set(df['Film'].unique()) - set(movies_in_db))

    for missing_movie in movies_to_fetch:
        add_new_movie(missing_movie, db_file)

    print('Movies data updated successfully.')


if __name__ == '__main__':
    pass#db_update('../data/clean_data.csv', '../data/movies.sqlite')
