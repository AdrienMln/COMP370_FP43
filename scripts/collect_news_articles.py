import requests
import json
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
import pandas as pd

NEWS_API_BASE_URL = "https://newsapi.org/v2/everything"
API_KEY = 'f2a6791826a24bb488ae92bd90e58696'
# '7ef2016e43554bb984ae1da0b1eaba9e'
MOVIE_DATA_FILENAME = 'movie_data.json'
# defining global base url which we query and then filter the results based on the parameters given to the function

def write_to_file(json_file, data):
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f)

def load_movie_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        content = f.read()
        return json.loads(content)

def fetch_latest_news(api_key, news_keywords):
    stop = datetime.now()
    start = stop - timedelta(days=31)

    # must format dates correctly to be in YYYY-MM-DD format
    stop_format, start_format = stop.strftime("%Y-%m-%dT%H:%M:%SZ"), start.strftime("%Y-%m-%dT%H:%M:%SZ")
    # here it is important to format both start and stop in terms of the time that we want to parse so that there is no discrepancy
    # set query parameters when making request
    query = ' AND '.join(news_keywords)

    query_parameters = {
        "apiKey": api_key, # parameter
        "q": query,
        "language": "en",
        "from": start_format,
        "to": stop_format,
        "sortBy": "publishedAt"
    }

    info = requests.get(NEWS_API_BASE_URL, params=query_parameters)

    if info.status_code == 200:
        news_articles = info.json()["articles"]
        return news_articles
    else:
        # If the request was not successful, raise an exception
        info.raise_for_status()

def main():
    the_marvels = fetch_latest_news(api_key=API_KEY, news_keywords=['The', 'Marvels', 'Nia', 'DaCosta'])
    the_holdovers = fetch_latest_news(api_key=API_KEY, news_keywords=['The', 'Holdovers', 'Alexander', 'Payne'])
    thg = fetch_latest_news(api_key=API_KEY, news_keywords=['The', 'Hunger', 'Games', 'The', 'Ballad', 'of', 'Songbirds', '&', 'Snakes', 'Francis', 'Lawrence'])
    priscilla = fetch_latest_news(api_key=API_KEY, news_keywords=['Priscilla', 'Sofia', 'Coppola'])
    thanksgiving = fetch_latest_news(api_key=API_KEY, news_keywords=['Thanksgiving', 'Eli', 'Roth'])
    saltburn = fetch_latest_news(api_key=API_KEY, news_keywords=['Saltburn', 'Emerald', 'Fennell'])

    movies = [the_marvels, the_holdovers, thg, priscilla, thanksgiving, saltburn] 

    # now we use a nested list comprehension to convert the movies list into a single level list containing all the articles
    articles_list = [article for movie in movies for article in movie]

    # remove articles that have invalid titles/descriptions
    valid_articles = list(filter(lambda article: article['title'] != "[Removed]" and article['description'] != '[Removed]', articles_list))

    # remove duplicate titles
    article_df = pd.DataFrame(valid_articles)
    unique_articles = article_df.drop_duplicates(subset='title')

    articles = unique_articles.to_dict(orient='records')
    articles_json = json.dumps(articles)

    movie_json_path = Path(__file__).parent.parent/'data'/MOVIE_DATA_FILENAME
    write_to_file(movie_json_path, articles_json)

if __name__ == '__main__':
    main()