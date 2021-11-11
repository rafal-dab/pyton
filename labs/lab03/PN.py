import argparse
from rich.console import Console
import rich.traceback
import requests
from bs4 import BeautifulSoup
import json

console = Console()
#console.clear()
rich.traceback.install()

base_url = 'https://zpppn.pl'

parser = argparse.ArgumentParser(description='Skrypt zapisuje dane ze strony ' + \
    base_url + ' do pliku w formacie JSON.')
parser.add_argument('file', help='nazwa pliku wyjściowego')
args = parser.parse_args()
fname = args.file

url = base_url + '/parki-narodowe'
req = requests.get(url)

soup = BeautifulSoup(req.text, 'html.parser')
div_parklist = soup.find('div', class_='parkList')
divs_parks = div_parklist.find_all('div', class_='listCol')
pn_list = [] #lista parków narodowych
for div in divs_parks:
    pn = {} # pojedynczy wpis na liście parków
    pn['nazwa'] = div.find('a')['title'] # nazwa parku
    url = base_url + div.find('a')['href']
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    div_park = soup.find('div', class_='parkPortfolioButtons')
    pn['www'] = div_park.find('a')['href'] # strona WWW
    kontakty = div_park.find_all('p')
    # szukanie danych kontaktowych:
    adr = ''
    tel = ''
    email = ''
    for p in kontakty:
        # telefon:
        if p.find('i', class_='fa-phone') is not None:
            tel = p.text.strip()
        # email:
        elif p.find('i', class_='fa-envelope-o') is not None:
            email = p.text.strip()
        # adres:
        else:
            if len(adr) == 0:
                adr += p.text.strip()
            else:
                adr += ', ' + p.text.strip()
    pn['adres'] = adr
    pn['telefon'] = tel
    pn['email'] = email

    pn_list.append(pn)

#console.print(pn_list)
with open(fname, 'w') as f:
    json.dump(pn_list, f)
