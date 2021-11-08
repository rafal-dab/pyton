import argparse
import re
from ascii_graph import Pyasciigraph
from collections import defaultdict

parser = argparse.ArgumentParser(description='Skrypt rysuje histogram wyrazów w pliku.')
parser.add_argument('file', help='nazwa pliku')
parser.add_argument('-n', '--number', help='dla ilu wyrazów wyświetlić histogram (domyślnie 10)', type=int, default=10)
parser.add_argument('-m', '--min', help='minimalna długość histogramowanego słowa (domyślnie 0)', type=int, default=0)
args = parser.parse_args()
fname = args.file
n = args.number
m = args.min

word_counter = defaultdict(int)

with open(fname, encoding='utf8') as f:
    for line in f:
        words = [re.sub("^[^0-9a-zżźćńółęąś]+|[^0-9a-zżźćńółęąś]+$", "", word) \
            for word in line.lower().strip().split()]
        for w in words:
            if len(w) >= m and w != '':
                word_counter[w] += 1
 
words.clear()
for k, v in word_counter.items():
    words.append((k, v))

words.sort(key = lambda e: e[1], reverse=True)

#for w in words[0:n]:
#    print(w)

graph = Pyasciigraph()
tytul = 'Histogram maksimum ' + str(n) + ' najczęściej występujących słów'
if m > 0:
    tytul += ' (o długości nie mniejszej niż ' + str(m) + ')'
tytul += ' w pliku ' + fname
for line in graph.graph(tytul, words[0:n]):
    print(line)
