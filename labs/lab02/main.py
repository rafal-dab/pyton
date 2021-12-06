import argparse
from rich.console import Console
import rich.traceback
from rich.progress import track
from os import mkdir
from time import localtime, strftime

import isinga

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

imc = isinga.IMC(n, J, T, B, d)

for i in track(range(k)):
    imc.savePNG(outdir + ("\\step%03d.png" % i))
    for j in range(n):
        imc.stepMC()

imc.savePNG(outdir + ("\\step%03d.png" % k))
