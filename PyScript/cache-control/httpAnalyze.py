import os
from subprocess import *
import sys

if len(sys.argv) < 2 or sys.argv[1] != 'analyze':
    tmps = os.listdir('tmp')

    for tmp in tmps:
        tmpBfile = os.path.join('httpBytes', tmp)
        tmpCfile = os.path.join('httpCounts', tmp)
        bfile = open(tmpBfile, 'w+')
        cfile = open(tmpCfile, 'w+')
        bfile.close()
        cfile.close()

    for tmp in tmps:
        call(['python3', 'httpBytes.py', tmp])
        call(['python3', 'httpCount.py', tmp])

bfiles = os.listdir('httpBytes')
cfiles = os.listdir('httpCounts')
bfracs = []
cfracs = []
bstr = ''
cstr = ''

def parse_portion(filename):
    a = open(filename, 'r').read().split('\n')[0]
    return float(a)

for bfile in bfiles:
    f = open(os.path.join('httpBytes', bfile), 'r').read()
    if f == '':
        os.remove(os.path.join('httpBytes',bfile))
        continue

for cfile in cfiles:
    f = open(os.path.join('httpCounts', cfile), 'r').read()
    if f == '':
        os.remove(os.path.join('httpCounts',cfile))
        continue

bfiles = os.listdir('bytes')
cfiles = os.listdir('counts')

for bfile in bfiles:
    frac = parse_portion(os.path.join('httpBytes',bfile))
    if frac != None:
        bfracs.append(frac)


for cfile in cfiles:
    frac = parse_portion(os.path.join('httpCounts',cfile))
    if frac != None:
        cfracs.append(frac)

bfracs.sort()
cfracs.sort()

i = 1
for bfrac in bfracs:
    bstr += '[{}, {}, null],\n'.format( bfrac, i / len(bfracs) )
    i += 1

i = 1
for cfrac in cfracs:
    cstr += '[{}, null, {}],\n'.format( cfrac, i / len(cfracs) )
    i += 1

print(bstr)
print("\n\n\n")
print(cstr)
