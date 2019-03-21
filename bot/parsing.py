import requests
from bs4 import BeautifulSoup


def http_get(search):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/72.0.3626.121 Safari/537.36'}
    conn = requests.get("https://concert.ua/ru/search-result?query=" + search, headers=headers)
    return conn.text


def parse_html(text):
    soup = BeautifulSoup(text, 'html.parser')
    all_events = soup.findAll(class_='event')
    event_dates = []
    for event in all_events:
            for td in event.findAll(class_='event__date'):
                event_dates.append(td.text)
