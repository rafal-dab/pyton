from rich.console import Console
import rich.traceback
from rich.progress import track
from os import mkdir
from time import localtime, strftime
import functools

import isinga

console = Console()
#console.clear()
rich.traceback.install()

n = 100 # rozmiar siatki
J = 0.05 # całka wymiany
T = 273.0 # temperatura
B = 0.1 # zewn. pole magn.
d = 0.5 # gęstość początkowa spinów w górę (1)
imc = isinga.IMC(n, J, T, B, d)
outdir = "out_" + strftime("%Y.%m.%d_%H-%M-%S", localtime())
#mkdir(outdir)
#imc.savePNG(outdir + "\\step000.png")

def runMC_decor(_func = None, repeat = 1):
    def decorator(func):
        @functools.wraps(func) # to powoduje, że nazwa pierwotnej funkcji jest zachowana
        def wrapper(*args, **kwars):
            console.log(f"[{colour}]Called {func.__name__}[/{colour}]")
            return func(*args, **kwars)

        return wrapper
    
    if _func is not None:
        return decorator(_func)

    return decorator

@runMC_decor
def runMC(i=1):
    for j in range(n):
        imc.stepMC()
    imc.savePNG(outdir + ("\\step%03d.png" % i))
