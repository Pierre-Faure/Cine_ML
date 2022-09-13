import requests
import json
import sqlite3
from movies.secrets import secrets
import sys

IMDB_API_SECRET = secrets.get('IMDB_API_KEY')
OMDB_API_SECRET = secrets.get('OMDB_API_KEY')
PROXIES = secrets.get('proxies')


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

    response = requests.request("GET", url, headers=headers, data=payload, proxies=PROXIES)
    data = json.loads(response.text)
    if data['errorMessage'] != '':
        print('Error from API: ' + data['errorMessage'])
        print('Quitting...')
        return
    elif not data["results"]:
        return -1
    else:
        return data['results'][0]['id']


def get_movie_details(title, date=""):
    # Fetching movie id
    movie_id = get_movie_id(title, date)
    if movie_id == -1:
        data = {'Response': 'False'}
    else:
        url = "http://www.omdbapi.com/?apikey=" + OMDB_API_SECRET + "&r=json&i=" + movie_id
        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload, proxies=PROXIES)
        data = json.loads(response.text)

    # Handling unidentified movies
    if data['Response'] != 'True':
        data = {'Title': title,
                'Year': 'N/A',
                'Rated': 'N/A',
                'Released': 'N/A',
                'Runtime': 'N/A',
                'Genre': 'N/A',
                'Director': 'N/A',
                'Writer': 'N/A',
                'Actors': 'N/A',
                'Plot': 'N/A',
                'Language': 'N/A',
                'Country': 'N/A',
                'Awards': 'N/A',
                'Poster': 'N/A',
                'Ratings': 'N/A',
                'Metascore': 'N/A',
                'imdbRating': 'N/A',
                'imdbVotes': 'N/A',
                'imdbID': 'N/A',
                'Type': 'N/A',
                'DVD': 'N/A',
                'BoxOffice': 'N/A',
                'Production': 'N/A',
                'Website': 'N/A',
                'Response': 'N/A'}
    return data


def save_to_db(data, title, filename):
    conn = sqlite3.connect(str(filename))
    cur = conn.cursor()

    full_title = data['Title']

    if (data['Year'] != 'N/A') & (isinstance(data['Year'], int)):
        year = int(data['Year'])
    else:
        year = -1
    if (data['Rated'] != 'N/A') & (isinstance(data['Rated'], str)):
        rated = data['Rated']
    else:
        rated = 'N/A'
    if (data['Released'] != 'N/A') & (isinstance(data['Released'], str)):
        released = data['Released']
    else:
        released = 'N/A'
    if (data['Runtime'] != 'N/A') & (isinstance(data['Runtime'], int)):
        runtime = int(data['Runtime'].split()[0])
    else:
        runtime = -1
    if (data['Country'] != 'N/A') & (isinstance(data['Country'], str)):
        country = data['Country']
    else:
        country = 'N/A'
    if (data['Genre'] != 'N/A') & (isinstance(data['Genre'], str)):
        genre = data['Genre']
    else:
        genre = 'N/A'
    if (data['Awards'] != 'N/A') & (isinstance(data['Awards'], str)):
        awards = data['Awards']
    else:
        awards = 'N/A'
    if (data['Metascore'] != 'N/A') & (isinstance(data['Metascore'], float)):
        metascore = float(data['Metascore'])
    else:
        metascore = -1
    if (data['imdbRating'] != 'N/A') & (isinstance(data['imdbRating'], float)):
        imdb_rating = float(data['imdbRating'])
    else:
        imdb_rating = -1

    cur.execute('''CREATE TABLE IF NOT EXISTS movie 
    (Title TEXT, FullTitle TEXT,  Year INTEGER, Rated TEXT, Released TEXT, Runtime INTEGER, Country TEXT, Genre TEXT, Awards TEXT, Metascore REAL, IMDBRating REAL)''')

    cur.execute('SELECT Title FROM movie WHERE Title = ? ', (title,))
    row = cur.fetchone()

    if row is None:
        cur.execute('''INSERT INTO movie (Title, FullTitle, Year, Rated, Released, Runtime, Country, Genre, Awards, Metascore, IMDBRating)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)''', (title,
                                                    full_title,
                                                    year,
                                                    rated,
                                                    released,
                                                    runtime,
                                                    country,
                                                    genre,
                                                    awards,
                                                    metascore,
                                                    imdb_rating))

    conn.commit()
    conn.close()


def add_new_movie(title, db_file, date=""):
    try:
        save_to_db(get_movie_details(title, date), title, db_file)
    except:
        print("[" + title + "]: Movie not added" + str(sys.exc_info()[0]))
        return
