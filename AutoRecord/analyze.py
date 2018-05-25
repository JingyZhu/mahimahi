import math
import os
from statistics import median

files = os.listdir('plTime')

def parse_error(filename):
    errors = []
    data = open(filename, 'r').read().split('\n')
    while data[-1] == '':
        del data[-1]
    i = 0
    while i < len(data):
        record = float(data[i].split('\t')[1])
        replay = float(data[i+1].split('\t')[1])
        i += 2
        error = abs(record-replay)/record
        errors.append(error)
    errors.sort()
    return median(errors)


for file in files:
    error = parse_error(os.path.join('plTime',file))
    print('{} error is : {}%'.format(file, error*100))