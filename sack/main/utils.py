from bs4 import BeautifulSoup
import requests
import re


def get_districts_stuttgart():
    url = 'http://onlinestreet.de/strassen/in-Stuttgart.html'
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'html.parser')
    for table in soup.findAll('table'):
        if 'blz' in table.get("class"):
            for index, tr in enumerate(table.findAll('tr')):
                if index == 0:
                    continue
                yield tr


def extract_district_from_tr(tr):
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


def get_streets_from_district(district):
    url = district.url_onlinestreet
    data = requests.get(url).text

    soup = BeautifulSoup(data, 'html.parser')
    for table in soup.findAll('table'):
        if 'strassen' in table.get('class'):
            for index, tr in enumerate(table.findAll('tr')):
                if index == 0:
                    continue
                yield tr


def extract_street_from_tr(tr):
    data = list(tr.children)
    p = re.compile(r'(?P<street>.*)\s+(?P<zipcode>[0-9]{5})\s+(?P<city>.*)')
    x = re.search(p, data[0].a.text)
    return {
        'url_onlinestreet': data[0].a['href'],
        'name': x.groupdict().get('street'), 
        'city': x.groupdict().get('city'),
        'zipcode': x.groupdict().get('zipcode'), 
    }


def add_street_to_database(data, district):
    from main.models import Street 
    street, created = Street.objects.get_or_create(district=district, **data)
    return street
