import requests
from bs4 import BeautifulSoup


def http_get(search):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/72.0.3626.121 Safari/537.36'}
    conn = requests.get("https://concert.ua/ru/search-result?query=" + search, headers=headers)
    return conn.text


def get_param(element: str, key='text', default=None, **kwargs: str) -> str:
    return getattr(element.find(**kwargs), key, default)


def parse_html(text: str) -> list:
    soup = BeautifulSoup(text, 'html.parser')
    event_info = []
    for event in soup.find_all('a', class_='event'):
        event_info.append({
            'name': get_param(event, class_='event__name'),
            'date': get_param(event, class_='event__date'),
            'location': get_param(event, class_='event__place'),
            'price': get_param(event, class_='event__price'),
            'link': 'https://concert.ua' + event['href'].replace('event', 'booking')
        })
    return event_info
