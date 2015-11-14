from bs4 import BeautifulSoup
import requests


def get_districts_stuttgart(data_source=None):
    if not data_source:
        url = 'http://onlinestreet.de/strassen/in-Stuttgart.html'
        data = requests.get(url).text
    else:
        data = open(data_source).read()
    soup = BeautifulSoup(data, 'html.parser')
    for table in soup.findAll('table'):
        if 'blz' in table.get("class"):
            for tr in table.findAll('tr'):
                yield tr


def extract_data_from_tr(tr):
    data = list(tr.children)
    return {
        'name': data[0].a.text,
        'url_onlinestreet': data[0].a['href'],
        'city': 'Stuttgart',
        'number_of_streets': data[1].text
    }


def add_district_to_database(data):
    from main.models import District
    district, created = District.objects.get_or_create(**data)
    return district
