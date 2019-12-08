##  This scripts scrapes the contents  we have in ../poets_glossary.py

from bs4 import BeautifulSoup
import requests
from pprint import pprint

url = 'http://ganjoor.net'
header= {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'}
req = requests.get(url, headers=header).text
soup = BeautifulSoup(req, "html.parser")

poets_glossary = {}
for poets in soup.findAll('div', attrs={'class': 'poet'}):
    english_name = poets.find('a')['href'].split('/')[3]
    persian_name = poets.find('a')['title']
    poets_glossary.update({english_name: persian_name})


pprint(poets_glossary)
