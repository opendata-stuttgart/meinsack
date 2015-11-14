from bs4 import BeautifulSoup
import requests

def get_districts_stuttgart(url=None):
    if not url:
        url = 'http://onlinestreet.de/strassen/in-Stuttgart.html'
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    print(soup)
