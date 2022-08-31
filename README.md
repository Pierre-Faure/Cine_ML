# Cine_ML
A tool to predict the activity of a french cinema according to external metadata (metadata on movies, on weather,...)
____________

## Data sources

- Movies: [IMDB API](https://imdb-api.com/API)
- Weather: [Historique-météo.net](https://www.historique-meteo.net/)
- Holidays: [Data.gouv.fr](https://www.data.gouv.fr/fr/datasets/jours-feries-en-france/)

## Additional tools

- Jours-feries-france: a package to get french holidays [Github page](https://github.com/etalab/jours-feries-france)
- Facebook Prophet : time series forecasting and analysis  [Prophet](https://facebook.github.io/prophet/)

## Goals of the project

Cinema employees and managers often know intuitively the aproximative number of spectators that could come to see a movie.
This guess is baased on experience, knowledge of the public habits or indications from distributors for example.

## Idea backlog

- Add Google trends data about movies (capture "hype")
- Add data from AlloCine such as average note, number of reviews, reviews average sentiment (sentiment analysis)