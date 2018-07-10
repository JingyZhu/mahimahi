from subprocess import *
import os
from os.path import join
import sys

mmpath = os.environ['mmpath']
FNULL = open(os.devnull, 'w')

http = 'http://'
https = 'https://'

def zero(web):
    traffic = open(join(mmpath, 'tmp', web, 'traffic.txt'), 'r').readlines()
    size = len(traffic)
    for i in range(size):
        traffic[i] = traffic[i].split('\t')
        traffic[i][1] = '0'
        traffic[i] = '\t'.join(traffic[i])
    new_traffic = open(join(mmpath,'tmp', web, 'traffic.txt'), 'w+')
    for t in traffic:
        new_traffic.write('{}\n'.format(t))
    new_traffic.close()

def round(num, web):
    call(['python3', 'transfer{}.py'.format(num), web])
    call(['python3', 'replay.py', url])
    call('rm -rf {}'.format(join(mmpath, 'tmp', web)), shell=True)
    call('cp -rf {} {}'.format(join(mmpath, 'tmp', web + '2'), join(mmpath, 'tmp', web)), shell=True)

webs = open('weblist', 'r').readlines()
while webs[-1] == "" or webs[-1] == '\n':
    del webs[-1]

webs = ['weblio.jp,True']# , 'wikia.com,True', 'ebay.co.uk', 'independent.co.uk,True']
count = 1
for times in range(3):
    for web in webs:
        web = web.strip('\n').split(',')
        url = https + web[0] if web[1] == 'True' else http + web[0]
        print('{}. {}'.format(count, url))
        if times == 0:
            print('Record')
            sys.stdout.flush()
            try:
                call(['python3', 'record.py', url], stdout=FNULL, stderr=STDOUT)
            except Exception as e:
                call(['pkill', 'chromium'])
                print("Something wrong with recording {}: {}".format(web[0], str(e)) )
            call( 'cp -rf {} {}'.format(join(mmpath, 'tmp', web[0]), join(mmpath, 'tmp', web[0]+'2')), shell=True)
        print('Replay')
        sys.stdout.flush()
        for i in range(1, 5):
            round(i, web[0])
        call(['python3', 'replay.py', url])
        zero(web[0])
        call(['python3', 'replay.py', url])
        call('rm -rf {}'.format(join(mmpath, 'tmp', web[0])), shell=True)
        call('cp -rf {} {}'.format(join(mmpath, 'tmp', web[0] + '2'), join(mmpath, 'tmp', web[0])), shell=True)
        count += 1
