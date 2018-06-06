from subprocess import *
import os

# call(['python3', 'get_web.py'])
epoch = 3

webf = open('weblist', 'r')
webs = webf.read().split('\n')
webf.close()

while webs[-1] == '':
    del webs[-1]

for web in webs:
    web = web.split(',')[0]
    f1 = open(os.path.join('bytes', web), 'w+')
    f1.close()
    f2 = open(os.path.join('counts', web), 'w+')
    f2.close()

for i in range(epoch):
    call(['python3', 'record.py'])
