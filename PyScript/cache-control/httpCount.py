"""cacheable http / all http (counts)"""
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
    elif line[0] == '3' and int(line[2]) != 0:
        total += 1
        if line[1] in http:
            httpStats += 1

counts = os.path.join('httpCounts', web)
cfile = open(counts, 'a')
if total != 0:
    cfile.write(str( httpStats / total ) + "\n" )
cfile.close()
