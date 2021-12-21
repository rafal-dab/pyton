from rich.console import Console
import rich.traceback
import requests
from bs4 import BeautifulSoup
import re
from PIL import Image
from os import mkdir, getpid
from time import time, localtime, strftime
from concurrent.futures import ProcessPoolExecutor

console = Console()
rich.traceback.install()
console.print(f'{__name__ = }, PID = {getpid()}')

base_url = 'http://www.if.pw.edu.pl/~mrow/dyd/wdprir/'

def process_img(fname, outdir):
    global base_url
    url = base_url + fname
    start = time()
    # console.print('PIL')
    req = requests.get(url, stream=True)
    im = Image.open(req.raw)
    im = im.convert("L")
    im.save(outdir + "\\" + fname)
    tm = time() - start
    console.print(("[PID=%d] Czas przetwarzania obrazka \"%s\": %.3f sek." % (getpid(), fname, tm)))
    # Tu dla porównania bezpośredni zapis obrazka bezpośrednio z URL
    # Obrazek zapisywany przez Pillow (bez żadnej konwersji) ma większy rozmiar na dysku, niż oryginał
    #
    # console.print('write')
    # req = requests.get(url)
    # with open(outdir + "\\org_" + fname, 'wb') as f:
    #     f.write(req.content)

if __name__ == '__main__':
    outdir = "out_" + strftime("%Y.%m.%d_%H-%M-%S", localtime())
    mkdir(outdir)
    start = time()
    req = requests.get(base_url)
    soup = BeautifulSoup(req.text, 'html.parser')
    imgs = soup.find_all('a', href=re.compile('img'))
    pool = ProcessPoolExecutor(len(imgs))
    fs = [pool.submit(process_img, i['href'], outdir) for i in imgs]
    rs = [f.result() for f in fs]
    tm = time() - start
    console.print(("[MAIN PID=%d] Czas przetwarzania: %.3f sek." % (getpid(), tm)))
