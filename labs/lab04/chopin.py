import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service, service
from selenium.webdriver.common.by import By
import time
import json

url = 'https://chopin2020.pl'
parser = argparse.ArgumentParser(description='Skrypt zapisuje dane ze strony ' + \
    url + ' do pliku w formacie JSON.')
parser.add_argument('file', help='nazwa pliku wyjściowego')
args = parser.parse_args()
fname = args.file

service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.get(url)
driver.execute_script('window.scrollTo(0, document.getElementById("scrollElement").previousSibling.offsetTop)')

winners = {} # zwycięzcy
# warstwy z danymi o zwycięzcach:
div_scrollEl = driver.find_element(By.ID, 'scrollElement')
divs = div_scrollEl.find_elements(By.XPATH, './div/div')
# przyciski do naciśnięcia:
div_buttons = div_scrollEl.find_element(By.XPATH, './following-sibling::div')
buttons = div_buttons.find_elements(By.TAG_NAME, 'div')
for button in buttons:
    button.click()
    time.sleep(1)
    for div in divs:
        el = div.find_elements(By.XPATH, './div/div/p')
        if len(el[0].text) == 0: # jeśli tekst jest pusty, tzn, że element jest niewidoczny
            continue
        info = el[1].text
        span = div.find_element(By.XPATH, './div/div/span')
        if len(span.text) > 0:
            info += ' (' + span.text + ')'
        winners[el[0].text] = info

#print(winners)
driver.close()
with open(fname, 'w') as f:
    json.dump(winners, f)
