import pandas as pd
from movies.movies_db_select import select_movie_by_title
from weather.weather_scrapping import daily_weather
from holidays.holiday_data import daily_holidays

input_file = 'data/clean_data.csv'
output_file = 'data/complete_data/complete_df.csv'
movies_db_file = 'data/movies.db' #'data/movies.sqlite'
holidays_data = 'data/holidays/feries_vacances.csv'


def create_dataset():
    """
    This function uses scripts from the packages 'holidays', 'movies' and 'weather' AND cinema data to create a complete
    dataframe that will be used in further steps
    :return: pandas dataframe
    """
    #df = pd.read_csv(input_file, sep=";")
    df = pd.read_csv(input_file, parse_dates=[['date', 'time']], dayfirst=True, encoding='utf-8')
    df['date_time'] = pd.to_datetime(df['date_time'])
    new_df = pd.DataFrame()
    for idx, row in df.iterrows():
        year = str(row['date_time'].year)
        month = f"{row['date_time']:%m}"
        day = f"{row['date_time']:%d}"

        # adding movie data
        print(row['Film'].encode('utf8').decode('mbcs').replace("'", "''"))
        row = row.append(select_movie_by_title(row['Film'].encode('utf8').decode('mbcs').replace("'", "''")).drop(columns=['Title']).iloc[0])

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
