from subprocess import *
import os

# call(['python3', 'get_web.py'])

webf = open('weblist', 'r')
webs = webf.read().split('\n')
webf.close()

while webs[-1] == '':
    del webs[-1]

for web in webs:
    web = web.split(',')[0]
    f = open(os.path.join('plTime', web), 'w+')
    f.close()

for i in range(4):
    print('Round: ' + str(i))
    call(['python3', 'record.py'])
    call(['python3', 'replay.py'])
