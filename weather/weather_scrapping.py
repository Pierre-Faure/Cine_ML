import pandas as pd
import requests
from bs4 import BeautifulSoup


def weather_request(year, month, day):
    url = "https://www.historique-meteo.net/france/lyonnais/saint-chamond/" + str(year) + "/" + str(month) + "/" + str(
        day) + "/"

    payload = {}
    headers = {}
    try:
        return requests.request("GET", url, headers=headers, data=payload).text
    except requests.exceptions.RequestException as e:
        print(e)
        return None


def data_scrapping(html_doc, year, month, day):
    soup = BeautifulSoup(html_doc, 'html.parser')
    if soup.find('title').string.find('404') == -1:
        tables = pd.read_html(soup.find(class_="table").prettify(), flavor='bs4')[0]
        tables = tables[[ str(day) + '/' + str(month) + '/' + str(year), 'Unnamed: 0']].T
        tables.columns = tables.iloc[1]
        tables = tables.drop('Unnamed: 0')
    else:
        tables = -1

    return tables


def daily_weather(year, month, day):
    return data_scrapping(weather_request(year, month, day), year, month, day)
