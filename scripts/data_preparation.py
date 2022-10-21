import pandas as pd
from movies.movies_db_select import select_movie_by_title
from weather.weather_scrapping import daily_weather
from holidays.holiday_data import daily_holidays
import numpy as np
from ast import literal_eval

input_file = 'data/clean_data.csv'  # 'data_test/seances.csv'
output_file = 'data/complete_data/complete_df.csv'
movies_db_file = 'data/movies.db'  # 'data/movies.sqlite'
holidays_data = 'data/holidays/feries_vacances.csv'


def create_dataset():
    """
    This function uses scripts from the packages 'holidays', 'movies' and 'weather' AND cinema data to create a complete
    dataframe that will be used in further steps
    :return: pandas dataframe
    """
    # df = pd.read_csv(input_file, sep=";")
    df = pd.read_csv(input_file, parse_dates=[['date', 'time']], dayfirst=True, encoding='utf-8')
    df['date_time'] = pd.to_datetime(df['date_time'])
    new_df = pd.DataFrame()
    list_rows = []
    for idx, row in df.iterrows():
        year = str(row['date_time'].year)
        month = f"{row['date_time']:%m}"
        day = f"{row['date_time']:%d}"

        # adding movie data
        # print(row['Film'].encode('utf8').decode('mbcs').replace("'", "''"))

        # row = row.append(select_movie_by_title(row['Film'].encode('utf8').decode('mbcs').replace("'", "''")).drop(columns=['Title']).iloc[0])
        df_movie = select_movie_by_title(row['Film'].replace("'", "''"))
        if not df_movie.empty:
            # row = row.append(df_movie.drop(columns=['Title']).iloc[0])
            row = pd.concat([row, df_movie.drop(columns=['Title']).iloc[0]], axis=0)

        # adding weather data
        # row = row.append(daily_weather(year, month, day).iloc[0])
        row = pd.concat([row, daily_weather(year, month, day).iloc[0]], axis=0)

        # adding holiday data
        # row = row.append(daily_holidays(year, month, day).drop(columns=['date']).iloc[0])
        row = pd.concat([row, daily_holidays(year, month, day).drop(columns=['date']).iloc[0]], axis=0)

        # new_df = new_df.append(row, ignore_index=True)

        list_rows.append(row)
    new_df = pd.concat([new_df, pd.DataFrame(list_rows)], axis=1)

    bool_cols = ['vacances_zone_a', 'vacances_zone_b', 'vacances_zone_c', 'ferie']
    # new_df[bool_cols] = new_df[bool_cols].astype('bool')

    # new_df['Released'] = pd.to_datetime(new_df['Released'])
    return new_df


def create_data_csv(df):
    df.to_csv(output_file, index=False)


def complete_data_recuperation(file_path):
    df = pd.read_csv(file_path)
    df['date_time'] = pd.to_datetime(df['date_time'])

    df['Nombre entrees'] = df[["Payants", "Gratuits"]].sum(axis=1)

    df['jour_semaine_seance'] = df['date_time'].dt.strftime("%A")
    df['jour_seance'] = df['date_time'].dt.strftime("%d")
    df['annee_seance'] = df['date_time'].dt.strftime("%G")
    df['heure_seance'] = df['date_time'].dt.strftime("%H")
    df['mois_seance'] = df['date_time'].dt.strftime("%B")

    s = df['Genre'].apply(lambda a: literal_eval(a) if pd.notnull(a) else a).explode()
    df = df.join(pd.crosstab(s.index, s))

    try:
        df['Taux remplissage'] = df['Taux remplissage'].str.rstrip('%').str.replace(',', '.').astype('float')
    except:
        print('Nothing to do')

    df = df.replace(['N/A', -1], np.nan)

    df["Heure du lever du soleil"] = pd.to_datetime(df["Heure du lever du soleil"], format='%H:%M:%S').dt.time
    df["Heure du coucher du soleil"] = pd.to_datetime(df["Heure du coucher du soleil"], format='%H:%M:%S').dt.time
    df["Durée du jour"] = pd.to_timedelta(df["Durée du jour"])
    df["Point de rosée"] = df["Point de rosée"].str.replace('°C', '').astype('float')
    df["Température maximale"] = df["Température maximale"].str.replace('°', '').astype('float')
    df["Température minimale"] = df["Température minimale"].str.replace('°', '').astype('float')
    df["Vitesse du vent"] = df["Vitesse du vent"].str.replace('km/h', '').astype('float')
    df["Température du vent"] = df["Température du vent"].str.replace('°', '').astype('float')
    df["Précipitations"] = df["Précipitations"].str.replace('mm', '').astype('float')
    df["Humidité"] = df["Humidité"].str.replace('%', '').astype('float')
    df["Visibilité"] = df["Visibilité"].str.replace('km', '').astype('float')
    df["Couverture nuageuse"] = df["Couverture nuageuse"].str.replace('%', '').astype('float')
    df["Pression"] = df["Pression"].str.replace('hPa', '').astype('float')

    df = df.rename(columns={
        "Température maximale": "Max_temp",
        "Température minimale": "Min_temp",
        "Vitesse du vent": "Vitesse_vent",
        "Température du vent": "Temp_vent",
        "Précipitations": "Precipitations",
        "Humidité": "Humidite",
        "Visibilité": "Visibilite",
        "Point de rosée": "Point de rosee",
        "Heure du lever du soleil": "Lever_soleil",
        "Heure du coucher du soleil": "Coucher_soleil",
        "Durée du jour": "Duree du jour",
        "L'avis de  historique-meteo.net": "Avis_meteo"
    })

    cat_cols = ['Salle', 'Film', 'Version', 'Relief', 'FullTitle', 'Adult', 'Release', 'Language',
                'Lever_soleil', 'Coucher_soleil',
                'Duree du jour', 'Avis_meteo', 'nom_vacances', 'jour_semaine_seance', 'jour_seance',
                'annee_seance', 'heure_seance', 'mois_seance']

    df[cat_cols] = df[cat_cols].astype('category')

    return df
