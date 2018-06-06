import math
import os
from statistics import median
from subprocess import *
import random

bfiles = os.listdir('bytes')
cfiles = os.listdir('counts')
bfracs = []
cfracs = []
bstr = ''
cstr = ''

def parse_portion(filename):
    frac = []
    data = open(filename, 'r').read().split('\n')
    while data[-1] == '':
        del data[-1]
    i = 0
    # print(filename + " " + str(len(data)))
    while i < len(data):
        try:
            frac.append(float(data[i]))
        except Exception as e:
            pass
        i += 1
    frac.sort()
    return None if frac == [] else median(frac)


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
    frac = parse_portion(os.path.join('bytes',bfile))
    if frac != None:
        bfracs.append(frac)

for cfile in cfiles:
    frac = parse_portion(os.path.join('counts',cfile))
    if frac != None:
        cfracs.append(frac)

bfracs.sort()
cfracs.sort()

i = 1
for bfrac in bfracs:
    bstr += '[{}, {}],'.format( bfrac, i / len(bfracs) )
    i += 1

i = 1
for cfrac in cfracs:
    cstr += '[{}, {}],'.format( cfrac, i / len(cfracs) )
    i += 1

print(bstr)
print(cstr)
