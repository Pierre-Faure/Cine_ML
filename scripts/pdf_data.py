import pandas as pd
import camelot
import os

path = os.getcwd()
pdf_dir = os.path.join(path, 'data', 'data_cine_pdf')
raw_data_path = os.path.join(path, 'data', 'raw_data', 'df_raw.csv')
files = ['2018.pdf', '2019.pdf', '2020.pdf', '2021.pdf', '2022.pdf']


def create_raw_csv():
    tables_list = []

    for file in files:
        file_dir = os.path.join(pdf_dir, file)
        tables_list.append(camelot.read_pdf(file_dir, pages='all'))

    df = pd.DataFrame()

    for tables in tables_list:
        for table in tables:
            df_table = table.df.copy()
            df_table.rename(columns=df_table.iloc[0], inplace=True)
            df_table.drop(df_table.index[0], inplace=True)
            df = pd.concat([df, df_table], ignore_index=True)

    df.to_csv('data/raw_data/df_raw.csv', index=False)


dfraw = pd.read_csv(raw_data_path)

df_cleaned = dfraw.drop([
    'Résa non \nvalidées',
    'Recette',
    'En \ncaisse',
    'En \nborne',
    'Sur \ninternet',
    'Aff \ncomplet',
    'Accès'
], axis=1)

df_cleaned = df_cleaned.rename(columns={"Spect. \nPayants": "Payants",
                           "Places \nlibres": "Places libres",
                           "Taux \nremplissage": "Taux remplissage"})

df_cleaned.to_csv('data/clean_data.csv', index=False)