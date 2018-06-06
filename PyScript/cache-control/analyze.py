import math
import os
from statistics import median
from subprocess import *
import random

bfiles = os.listdir('bytes')
cfiles = os.listdir('counts')
bfracs = []
bhttp = []
cfracs = []
chttp = []
bstr = ''
cstr = ''

def parse_portion(filename):
    frac = []
    http = []
    data = open(filename, 'r').read().split('\n')
    while data[-1] == '':
        del data[-1]
    # print(filename + " " + str(len(data)))
    for datus in data:
        try:
            datus = datus.split(' ')
            if datus[0] == 'all:':
                frac.append(float(datus[1]))
            elif datus[0] == 'http:':
                http.append(float(datus[1]))
        except Exception as e:
            pass
    frac.sort()
    datus.sort()
    return None if frac == [] or http == [] else (median(frac), median(http))


for bfile in bfiles:
    f = open(os.path.join('bytes', bfile), 'r').read()
    if f == '':
        os.remove(os.path.join('bytes',bfile))
        continue

for cfile in cfiles:
    f = open(os.path.join('counts', cfile), 'r').read()
    if f == '':
        os.remove(os.path.join('counts',cfile))
        continue

bfiles = os.listdir('bytes')
cfiles = os.listdir('counts')

for bfile in bfiles:
    frac, http = parse_portion(os.path.join('bytes',bfile))
    if frac != None:
        bfracs.append(frac)
    if http != None:
        bhttp.append(http)


for cfile in cfiles:
    frac, http = parse_portion(os.path.join('counts',cfile))
    if frac != None:
        cfracs.append(frac)
    if http != None:
        chttp.append(http)

bfracs.sort()
cfracs.sort()
bhttp.sort()
chttp.sort()

i = 1
for bfrac in bfracs:
    bstr += '[{}, {}, null],'.format( bfrac, i / len(bfracs) )
    i += 1

i = 1
for bh in bhttp:
    bstr += '[{}, null, {}],'.format( bh, i / len(bhttp) )
    i += 1

i = 1
for cfrac in cfracs:
    cstr += '[{}, {}, null],'.format( cfrac, i / len(cfracs) )
    i += 1

i = 1
for ch in chttp:
    cstr += '[{}, null, {}],'.format( ch, i / len(chttp) )
    i += 1

print(bstr)
print(cstr)
