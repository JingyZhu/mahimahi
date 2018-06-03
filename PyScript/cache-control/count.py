import sys
import os

total = 0
cachable = 0
cached = {}

web = sys.argv[1]
tmp = os.path.join('tmp', web)

rfile = open(tmp, 'r').read().split('\n')
while rfile[-1] == '':
    del rfile[-1]

for line in rfile:
    line = line.split('\t')
    if line[0] == '3':
        total += 1
        if line[1] in cached:
            cachable += 1
    elif line[0] == '2':
        cached[line[1]] = 0

counts = os.path.join('counts', web)
cfile = open(counts, 'a')

cfile.write(str( cachable / total ) + "\n")
cfile.close()
# print('cachable: {}\ntotal: {}\nfraction: {}%'.format(cachable, total, cachable / total * 100))