import pandas as pd
from jours_feries_france import JoursFeries


def get_holidays(input_file):
    """
    get a dataframe containing the dates of metropolitan french school holidays and civil holidays
    :param input_file: (str) raw data path
    :return:
    """
    df = pd.read_csv(input_file)
    df['date'] = pd.to_datetime(df['date'])
    df['ferie'] = df.apply(lambda row: JoursFeries.is_bank_holiday(row['date'], zone="Métropole"), axis=1)
    return df


def create_holidays_csv(df, output_file):
    df.to_csv(output_file, index=False)


if __name__ == "__main__":
    create_holidays_csv(get_holidays('../data/holidays/vacances_scolaires.csv'), '../data/holidays/feries_vacances.csv')
