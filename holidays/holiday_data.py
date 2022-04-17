import pandas as pd
from jours_feries_france import JoursFeries

holidays_file = 'data/holidays/feries_vacances.csv'
vacances_file = 'data/holidays/vacances_scolaires.csv'


def get_holidays(input_file):
    """
    get a dataframe containing the dates of metropolitan french school holidays and civil bank holidays
    :param input_file: (str) raw data path
    :return: pandas dataframe
    """
    df = pd.read_csv(input_file)
    df['date'] = pd.to_datetime(df['date'])
    df['ferie'] = df.apply(lambda row: JoursFeries.is_bank_holiday(row['date'], zone="Métropole"), axis=1)
    return df


def create_holidays_csv(df, output_file):
    """
    Function to save dataframe to csv file
    :param df: pandas dataframe
    :param output_file: path to csv file
    :return:
    """
    df.to_csv(output_file, index=False)


def update_holidays():
    """
    Function that update the holidays csv file
    :return:
    """
    try:
        create_holidays_csv(get_holidays(vacances_file), holidays_file)
        print('Holidays data updated successfully.')
    except:
        print('Updating holidays raised an error.')


def daily_holidays(year, month, day):
    df = pd.read_csv(holidays_file)
    df['date'] = pd.to_datetime(df['date'])

    return df[df['date'] == str(year) + '-' + str(month) + '-' + str(day)]


if __name__ == "__main__":
    pass
