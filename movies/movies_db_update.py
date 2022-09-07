import pandas as pd
from movies.imdb import add_new_movie


def db_update(input_file, db_file):
    df = pd.read_csv(input_file, parse_dates=[['date', 'time']], dayfirst=True, encoding='utf-8')
    for movie in df['Film'].unique():
        add_new_movie(movie, db_file)
    print('Movies data updated successfully')


if __name__ == '__main__':
    db_update('../data/clean_data.csv', '../data/movies.sqlite')

