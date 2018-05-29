import math
import os
from statistics import median
from subprocess import *

files = os.listdir('plTime')
errors = []

def parse_error(filename):
    errors = []
    data = open(filename, 'r').read().split('\n')
    while data[-1] == '':
        del data[-1]
    i = 0
    # print(filename + " " + str(len(data)))
    while i < len(data):
        # print(str(i))
        record = float(data[i].split('\t')[1])
        replay = float(data[i+1].split('\t')[1])
        i += 2
        error = abs(record-replay)/record
        errors.append(error)
    errors.sort()
    return median(errors)

def parse_server(filename):
    fserver = open(filename, 'r').read().split('\n')
    while fserver[-1] == '':
        del fserver[-1]
    return len(fserver)

for file in files:
    f = open(os.path.join('plTime', file), 'r').read()
    if f == '':
        os.remove(os.path.join('plTime',file))
        continue
    f = f.split('\n')
    while f[-1] == '':
        del f[-1]
    if len(f) % 2 == 1:
        os.remove(os.path.join('plTime', file))
files = os.listdir('plTime')

for file in files:
    print(file)
    error = parse_error(os.path.join('plTime',file))
    num_servers = parse_server((os.path.join('RTT', file)))
    print('{} (server {}) error is :\t{}%'.format(file, num_servers, error*100))
    errors.append(error)
    call(['cat', os.path.join('plTime', file)])
    print('RTT: ')
    call(['cat', os.path.join('RTT', file)])

errors.sort()
