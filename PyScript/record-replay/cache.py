from subprocess import *
import os
from os.path import join
import sys

mmpath = os.environ['mmpath']
FNULL = open(os.devnull, 'w')

http = 'http://'
https = 'https://'
name = ['nocache', 'httpcache', 'anycache', 'dummy']

def zero(web):
    traffic = open(join(mmpath, 'tmp', web, 'traffic.txt'), 'r').readlines()
    size = len(traffic)
    for i in range(size):
        traffic[i] = traffic[i].split('\t')
        traffic[i][1] = '0.01'
        traffic[i] = '\t'.join(traffic[i])
    new_traffic = open(join(mmpath,'tmp', web, 'traffic.txt'), 'w+')
    for t in traffic:
        new_traffic.write('{}\n'.format(t))
    new_traffic.close()

def round(num, web):
    call(['python3', 'transfer{}.py'.format(num), web])
    call(['python3', 'replay.py', url, name[num-1]])
    call('rm -rf {}'.format(join(mmpath, 'tmp', web)), shell=True)
    call('cp -rf {} {}'.format(join(mmpath, 'tmp', web + '2'), join(mmpath, 'tmp', web)), shell=True)

webs = open('weblist2', 'r').readlines()
while webs[-1] == "" or webs[-1] == '\n':
    del webs[-1]

# webs = ['bestonlinerpggames.com'] 
count = 1
times = 1
for times in range(1, 4):
    for web in webs:
        web = web.strip('\n').split(',')
        url = https + web[0] if web[1] == 'True' else http + web[0]
        print('{}. {}'.format(count, url))
        if times == 1:
            print('Record')
            sys.stdout.flush()
            try:
                call(['python3', 'record.py', url], stdout=FNULL, stderr=STDOUT)
            except Exception as e:
                call(['pkill', 'chromium'])
                print("Something wrong with recording {}: {}".format(web[0], str(e)) )
            call( 'cp -rf {} {}'.format(join(mmpath, 'tmp', web[0]), join(mmpath, 'tmp', web[0]+'2')), shell=True)
        try:
            print('Replay ' + str(times))
            sys.stdout.flush()
            for i in range(1, 4):
                round(i, web[0])
            # call(['python3', 'replay.py', url, 'origin'])
            # zero(web[0])
            # call(['python3', 'replay.py', url])
            #call('rm -rf {}'.format(join(mmpath, 'tmp', web[0])), shell=True)
            #call('cp -rf {} {}'.format(join(mmpath, 'tmp', web[0] + '2'), join(mmpath, 'tmp', web[0])), shell=True)
        except Exception as e:
            print("something wrong: " + str(e))
            continue
        count += 1
