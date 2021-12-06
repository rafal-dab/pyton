import random
import math
from PIL import Image, ImageDraw

class IMC:
    def __init__(self, n, J, T, B, d):
        self._n = n
        self._J = J
        self._beta = 1 / (1.38e-23 * T)
        self._B = B
        self._d = d # początkowa gęstość spinów w górę (1)
        self._N = n * n # ilość wszystkich komórek
        self._H = 0.0 # hamiltomian aktualnego stanu
        #  1 - spin w górę
        # -1 - spin w dół
        # najpierw wszystkie spiny w dół:
        self._matrix = [[-1 for i in range(n)] for j in range(n)]
        # obliczenie ile spinów ma być w górę:
        n_up = int(self._d * self._N)
        # na losowych pozycjach spiny w górę:
        for k in random.sample(range(self._N), n_up):
            i = int(k / self._n)
            j = k % self._n
            self._matrix[i][j] = 1
        # obliczenie hamiltonianu:
        self._calcH()
    
    def getMatrix(self):
        return self._matrix

    def savePNG(self, fname):
        # zielony - spin w górę (1)
        # brązowy - spin w dół (-1)
        # obliczenie rozmiaru obrazka - każda komórka 20x20 px:
        px_size = 20
        PNGsize = self._n * px_size
        image = Image.new('RGB', (PNGsize, PNGsize), "Maroon")
        draw = ImageDraw.Draw(image)
        for i in range(self._n):
            for j in range(self._n):
                if self._matrix[i][j] == 1:
                    x = j * px_size
                    y = i * px_size
                    draw.rectangle((x, y, x+px_size, y+px_size), "Green")

        image.save(fname)

    def _calcH(self):
        # oblicza hamiltonian i zwraca go jednocześnie
        H = 0.0
        # oddziaływania pomiędzy komórkami
        # w wierszach poziomo:
        for i in range(self._n):
            for j in range(self._n-1):
                H += self._matrix[i][j] * self._matrix[i][j+1]
        # w kolumnach pionowo:
        for j in range(self._n):
            for i in range(self._n-1):
                H += self._matrix[i][j] * self._matrix[i+1][j]
        H *= -self._J

        # oddziaływania z polem B:
        Hb = 0.0
        for i in range(self._n):
            for j in range(self._n):
                Hb += self._matrix[i][j]
        H += -self._B * Hb

        self._H = H
        return self._H

    def stepMC(self):
        # pojedynczy (mikro)krok symulacji
        H = self._H
        i = random.randrange(self._n)
        j = random.randrange(self._n)
        self._matrix[i][j] *= -1
        newH = self._calcH()
        deltaH = newH - H
        if deltaH > 0:
            p = math.exp(-self._beta * deltaH)
            if random.random() > p:
                # brak akceptacji zmiany - powrót do poprzedniego stanu
                self._matrix[i][j] *= -1
                self._H = H
