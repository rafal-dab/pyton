import numpy as np
import math

from numba import int64, float64, prange
from numba.experimental import jitclass

@jitclass
class IMC:
    _n: int64
    _J: float64
    _T: float64
    _B: float64
    _d: float64
    _beta: float64
    _N: int64
    _H: float64
    matrix: int64[:,:]

    def __init__(self, n: int64, J: float64, T: float64, B: float64, d: float64):
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
        self.matrix = np.full((n, n), -1)
        # obliczenie ile spinów ma być w górę:
        n_up = int(self._d * self._N)
        # na losowych pozycjach spiny w górę:
        for k in np.random.choice(self._N, n_up, replace=False):
            i = int(k / self._n)
            j = k % self._n
            self.matrix[i][j] = 1
        # obliczenie hamiltonianu:
        self._calcH()
    
    def getMatrix(self) -> int64[:,:]:
        return self.matrix

    def _calcH(self) -> float64:
        # oblicza hamiltonian i zwraca go jednocześnie
        H = 0.0
        # oddziaływania pomiędzy komórkami
        # w wierszach poziomo:
        for i in prange(self._n):
            for j in prange(self._n-1):
                H += self.matrix[i][j] * self.matrix[i][j+1]
        # w kolumnach pionowo:
        for j in prange(self._n):
            for i in prange(self._n-1):
                H += self.matrix[i][j] * self.matrix[i+1][j]
        H *= -self._J

        # oddziaływania z polem B:
        Hb = 0.0
        for i in prange(self._n):
            for j in prange(self._n):
                Hb += self.matrix[i][j]
        H += -self._B * Hb

        self._H = H
        return self._H

    def stepMC(self):
        # pojedynczy (mikro)krok symulacji
        H = self._H
        i = np.random.randint(0, self._n)
        j = np.random.randint(0, self._n)
        self.matrix[i][j] *= -1
        newH = self._calcH()
        deltaH = newH - H
        if deltaH > 0:
            p = math.exp(-self._beta * deltaH)
            if np.random.random() > p:
                # brak akceptacji zmiany - powrót do poprzedniego stanu
                self.matrix[i][j] *= -1
                self._H = H
