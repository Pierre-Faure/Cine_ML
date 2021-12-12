import requests
import json
import sqlite3
from movies.secrets import secrets

IMDB_API_SECRET = secrets.get('IMDB_API_KEY')
OMDB_API_SECRET = secrets.get('OMDB_API_KEY')


def get_movie_id(title, date=""):
    """
    get the IMDB id of a movie by its title and (optional) its date
    :param title: (str) the title of the movie
    :param date: (str) the release date of the movie. Helps to identify the right movie in results
    :return: (str) the IMDB id of the movie
    """
    url = "https://imdb-api.com/fr/API/SearchMovie/" + IMDB_API_SECRET + "/" + title + date
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    return data['results'][0]['id']


def get_movie_details(title, date=""):
    url = "http://www.omdbapi.com/?apikey=" + OMDB_API_SECRET + "&r=json&i=" + get_movie_id(title, date)
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    return data


def save_to_db(data, filename):
    conn = sqlite3.connect(str(filename))
    cur = conn.cursor()

    title = data['Title']

    if data['Year'] != 'N/A':
        year = int(data['Year'])
    if data['Runtime'] != 'N/A':
        runtime = int(data['Runtime'].split()[0])
    if data['Country'] != 'N/A':
        country = data['Country']
    if data['Metascore'] != 'N/A':
        metascore = float(data['Metascore'])
    else:
        metascore = -1
    if data['imdbRating'] != 'N/A':
        imdb_rating = float(data['imdbRating'])
    else:
        imdb_rating = -1

    cur.execute('''CREATE TABLE IF NOT EXISTS movie 
    (Title TEXT, Year INTEGER, Runtime INTEGER, Country TEXT, Metascore REAL, IMDBRating REAL)''')

    cur.execute('SELECT Title FROM movie WHERE Title = ? ', (title,))
    row = cur.fetchone()

    if row is None:
        cur.execute('''INSERT INTO movie (Title, Year, Runtime, Country, Metascore, IMDBRating)
                VALUES (?,?,?,?,?,?)''', (title, year, runtime, country, metascore, imdb_rating))
    else:
        print("Record already found. No update made.")

    conn.commit()
    conn.close()
