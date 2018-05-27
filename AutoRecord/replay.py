from subprocess import *
import os
import sys

http = 'http://www.'
https = 'https://www.'
FNULL=open(os.devnull, 'w')
web_list = open('weblist', 'r').read().split('\n')
while web_list[-1] == "":
    del web_list[-1]

mmwebreplay = os.path.join(os.environ['mmpath'], 'usr/bin/mm-webreplay')
repo =  os.path.join(os.environ['mmpath'], 'tmp')

i = 0
for web in web_list:
    web = web.split(',')
    i += 1
    sys.stdout.flush()
    aurl = https + web[0] if bool(web[1]) else http + web[0]
    url = http + web[0]
    print(str(i) + " replay: " + aurl)
    web = web[0]
    call([mmwebreplay, os.path.join(repo, web), 'python3', 'chrome.py', url], env=os.environ.copy(), stdout=FNULL, stderr=STDOUT)
