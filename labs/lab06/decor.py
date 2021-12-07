from rich.console import Console
import rich.traceback
from rich.progress import track
from os import mkdir
from time import localtime, strftime, time
import functools

import isinga

console = Console()
#console.clear()
rich.traceback.install()

n = 100 # rozmiar siatki
J = 0.005 # całka wymiany
T = 273.0 # temperatura
B = 0.1 # zewn. pole magn.
d = 0.5 # gęstość początkowa spinów w górę (1)
imc = isinga.IMC(n, J, T, B, d)
outdir = "out_" + strftime("%Y.%m.%d_%H-%M-%S", localtime())
mkdir(outdir)
imc.savePNG(outdir + "\\step000.png")

def runMC_decor(_func = None, repeat = 1):
    def decorator(func):
        @functools.wraps(func) # to powoduje, że nazwa pierwotnej funkcji jest zachowana
        def wrapper(*args, **kwars):
            tsum = 0.0
            for m in track(range(1, repeat+1)):
                kwars['i'] = m
                # console.log(f"Called {func.__name__} {m = } {args = } {kwars = }")
                before = time()
                func(*args, **kwars)
                duration = time() - before
                tsum += duration
            avg = tsum / repeat
            console.print(f'Średni czas wywołania funkcji "{func.__name__}": {("%.3f" % avg)} sek.')
            console.print(f'Liczba wywołań: {repeat}')
            return func(*args, **kwars)

        return wrapper
    
    if _func is not None:
        return decorator(_func)

    return decorator

@runMC_decor(repeat = 5)
# @runMC_decor
def runMC(i=1):
    for j in range(n):
        imc.stepMC()
    imc.savePNG(outdir + ("\\step%03d.png" % i))

runMC()