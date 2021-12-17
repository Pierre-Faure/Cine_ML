import pandas as pd
from movies.movies_db_select import select_movie_by_title
from weather.weather_scrapping import daily_weather
from holidays.holiday_data import daily_holidays

input_file = 'data_test/seances.csv'
output_file = 'data_test/df_test.csv'
movies_db_file = 'data/movies.sqlite'
holidays_data = 'data/holidays/feries_vacances.csv'


def create_dataset():
    df = pd.read_csv(input_file, sep=";")
    df['date'] = pd.to_datetime(df['date'])
    new_df = pd.DataFrame()
    for idx, row in df.iterrows():
        year = str(row['date'].year)
        month = f"{row['date']:%m}"
        day = f"{row['date']:%d}"

        # adding movie data
        row = row.append(select_movie_by_title(row['film']).drop(columns=['Title']).iloc[0])

        # adding weather data
        row = row.append(daily_weather(year, month, day).iloc[0])

        # adding holiday data
        row = row.append(daily_holidays(year, month, day).drop(columns=['date']).iloc[0])

        new_df = new_df.append(row, ignore_index=True)

    bool_cols = ['vacances_zone_a', 'vacances_zone_b', 'vacances_zone_c', 'ferie']
    new_df[bool_cols] = new_df[bool_cols].astype('bool')

    new_df['Released'] = pd.to_datetime(new_df['Released'])
    return new_df


def create_data_csv(df):
    df.to_csv(output_file, index=False)
