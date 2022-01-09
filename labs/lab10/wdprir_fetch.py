from rich.console import Console
import rich.traceback
import requests
from bs4 import BeautifulSoup
import re
from os import mkdir
from time import time, localtime, strftime

console = Console()
rich.traceback.install()

base_url = 'http://www.if.pw.edu.pl/~mrow/dyd/wdprir/'

def main():
    resp = requests.get(base_url)
    html = resp.text
    soup = BeautifulSoup(html, 'html.parser')
    imgs = soup.find_all('a', href=re.compile('img'))
    imgs = [i['href'] for i in imgs]

    for img in imgs:
        start = time()
        url = base_url + img
        print(url)
        resp = requests.get(url)
        with open(outdir + "\\" + img, 'wb') as f:
            f.write(resp.content)
        tm = time() - start
        console.print(("\tCzas pobierania obrazka \"%s\": %.3f sek." % (img, tm)))

outdir = "out_" + strftime("%Y.%m.%d_%H-%M-%S", localtime())
mkdir(outdir)
start = time()

main()

tm = time() - start
console.print(("\nCzas całkowity: %.3f sek." % (tm)))
