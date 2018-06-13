import sys
import os
from urllib.parse import urlparse

total = 0
httpStats = 0
http = {}

web = sys.argv[1]
tmp = os.path.join('tmp', web)

rfile = open(tmp, 'r').read().split('\n')
while rfile[-1] == '':
    del rfile[-1]

for line in rfile:
    line = line.split('\t')
    if line[0] == '1':
        scheme = urlparse(line[2]).scheme
        if scheme == 'http':
            http[line[1]] = 0
    elif line[0] == '3':
        total += int(line[2])
        if line[1] in http:
            httpStats += int(line[2])

byte = os.path.join('httpBytes', web)
bfile = open(byte, 'a')
if total != 0:
    bfile.write(str(httpStats / total) + "\n" )
bfile.close()
