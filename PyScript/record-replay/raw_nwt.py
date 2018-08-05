"""
Used for plot the original vs modified settings
"""
import math
import os
from statistics import median
from subprocess import *
from os.path import join

def max(a, b):
	if a < b:
		return b
	return a

files = os.listdir('plTime')

modified_PLT = [[] for i in range(len(files))]
modified_NWT = [ [] for i in range(len(files)) ]
origin_PLT = [ [] for i in range(len(files)) ]
origin_NWT = [ [] for i in range(len(files)) ]

modified_proportion = [ [] for i in range(len(files)) ]
origin_proportion = [ [] for i in range(len(files)) ]

for i in range(0, 1*4, 4):
	for j in range(len(files)):
		file = files[j]
		f = open(join('plTime', file), 'r').readlines()
		m_p = float(f[i+0].split('\t')[1])
		m_n = float(f[i+1].split('\t')[1])
		o_p = float(f[i+2].split('\t')[1])
		o_n = float(f[i+3].split('\t')[1])
		m_pro = m_n/m_p
		o_pro = o_n/o_p
        
		modified_PLT[j].append(m_p)
		modified_NWT[j].append(m_n)
		origin_PLT[j].append(o_p)
		origin_NWT[j].append(o_n)

		modified_proportion[j].append(m_pro)
		origin_proportion[j].append(o_pro)



for j in range(len(files)):
    modified_PLT[j] = median(modified_PLT[j])
    modified_NWT[j] = median(modified_NWT[j])
    origin_PLT[j] = median(origin_PLT[j])
    origin_NWT[j] = median(origin_NWT[j])
    modified_proportion[j] = median(modified_proportion[j])
    origin_proportion[j] = median(origin_proportion[j])


modified_PLT.sort()
modified_NWT.sort()
origin_PLT.sort()
origin_NWT.sort()


strr = ""  # Both line


size = len(origin_NWT)
# PLT read
for i in range(size):
	strr += '[{}, {}, null, null, null],\n'.format(modified_PLT[i], (i+1)/size)

for i in range(size):
    strr += '[{}, null, {}, null, null],\n'.format(modified_NWT[i], (i+1)/size)

for i in range(size):
    strr += '[{}, null, null, {}, null],\n'.format(origin_PLT[i], (i+1)/size)

for i in range(size):
    strr += '[{}, null, null, null, {}],\n'.format(origin_NWT[i], (i+1)/size)

print(strr)
