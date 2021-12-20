import argparse
from rich.console import Console
import rich.traceback
from rich.progress import track
from os import mkdir
from time import localtime, strftime
from PIL import Image, ImageDraw

import isinga_numba

console = Console()
#console.clear()
rich.traceback.install()

parser = argparse.ArgumentParser(description='Skrypt wykonuje symulację modelu Isinga 2D metodą Monte Carlo.')
parser.add_argument('n', help='rozmiar siatki', type=int)
parser.add_argument('J', help='wartość J', type=float)
parser.add_argument('T', help='temperatura (K)', type=float)
parser.add_argument('B', help='wartość zewnętrznego pola', type=float)
parser.add_argument('k', help='liczba kroków symulacji', type=int)
parser.add_argument('-d', '--density', help='początkowa gęstość spinów w górę (domyślnie 0.5)', type=float, default=0.5)
args = parser.parse_args()
n = args.n
J = args.J
T = args.T
B = args.B
k = args.k
d = args.density

outdir = "out_" + strftime("%Y.%m.%d_%H-%M-%S", localtime())
mkdir(outdir)

def savePNG(matrix, fname):
    # zielony - spin w górę (1)
    # brązowy - spin w dół (-1)
    # obliczenie rozmiaru obrazka - każda komórka 20x20 px:
    global n
    px_size = 20
    PNGsize = n * px_size
    image = Image.new('RGB', (PNGsize, PNGsize), "Maroon")
    draw = ImageDraw.Draw(image)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 1:
                x = j * px_size
                y = i * px_size
                draw.rectangle((x, y, x+px_size, y+px_size), "Green")

    image.save(fname)

imc = isinga_numba.IMC(n, J, T, B, d)

for i in track(range(k)):
    savePNG(imc.getMatrix(), outdir + ("\\step%03d.png" % i))
    for j in range(n):
        imc.stepMC()

savePNG(imc.getMatrix(), outdir + ("\\step%03d.png" % k))
