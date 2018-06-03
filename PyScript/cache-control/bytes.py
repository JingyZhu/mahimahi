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
        total += int(line[2])
        if line[1] in cached:
            cachable += int(line[2])
    elif line[0] == '2':
        cached[line[1]] = 0

byte = os.path.join('bytes', web)
bfile = open(byte, 'a')

bfile.write(str( cachable / total ) + "\n")
bfile.close()