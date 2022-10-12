import pandas as pd
import requests
from bs4 import BeautifulSoup
from movies.secrets import secrets

PROXIES = secrets.get('proxies')


def weather_request(year, month, day):
    url = "https://www.historique-meteo.net/france/lyonnais/saint-chamond/" + str(year) + "/" + str(month) + "/" + str(
        day) + "/"

    payload = {}
    headers = {}
    try:
        return requests.request("GET", url, headers=headers, data=payload, proxies=PROXIES).text
    except requests.exceptions.RequestException as e:
        print(e)
        return None


def data_scrapping(html_doc, year, month, day):
    col_list = ['Température maximale', 'Température minimale', 'Vitesse du vent', 'Température du vent', 'Humidité',
                'Visibilité', 'Couverture nuageuse', 'Indice de chaleur', 'Point de rosée', 'Pression',
                'Heure du lever du soleil', 'Heure du coucher du soleil', 'Durée du jour',
                "L'avis de  historique-meteo.net"]
    if html_doc is not None:
        soup = BeautifulSoup(html_doc, 'html.parser')
        if soup.find('title').string.find('404') == -1:
            tables = pd.read_html(soup.find(class_="table").prettify(), flavor='bs4')[0]
            tables = tables[[str(day) + '/' + str(month) + '/' + str(year), 'Unnamed: 0']].T
            tables.columns = tables.iloc[1]
            tables = tables.drop('Unnamed: 0')
        else:
            tables = pd.DataFrame(data=[None] * 14).T
            tables.columns = col_list

        return tables
    else:
        tables = pd.DataFrame(data=[None] * 14).T
        tables.columns = col_list
        return tables


def daily_weather(year, month, day):
    return data_scrapping(weather_request(year, month, day), year, month, day)
