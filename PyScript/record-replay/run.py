from subprocess import *
import os
import sys

epoch = 1

# call(['python3', 'get_web.py'])
ifcon = True if len(sys.argv)==2 and sys.argv[1] == 'continue' else False
webf = open('weblist', 'r')
webs = webf.read().split('\n')
webf.close()

while webs[-1] == '':
    del webs[-1]

if not ifcon:
    for web in webs:
        web = web.split(',')[0]
        f = open(os.path.join('plTime', web), 'w+')
        f.close()

for i in range(epoch):
    print('Round: ' + str(i))
    call(['python3', 'record_all.py'])
    call(['python3', 'replay_all.py'])
