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
mmlink = os.path.join(os.environ['mmpath'], 'usr/bin/mm-link')
mmdelay = os.path.join(os.environ['mmpath'], 'usr/bin/mm-delay')
repo =  os.path.join(os.environ['mmpath'], 'tmp')

i = 0
for web in web_list:
    web = web.split(',')
    i += 1
    sys.stdout.flush()
    url = https + web[0] if bool(web[1]) else http + web[0]
    # url = http + web[0]
    print(str(i) + " replay: " + url)
    web = web[0]
    try:
        call([mmwebreplay, os.path.join(repo, web), mmdelay, '0', os.path.join(repo, web), '--',  mmlink, 'trace_file', 'trace_file', '--', 'python3', 'chrome.py', url], timeout=30, env=os.environ.copy(), stdout=FNULL, stderr=STDOUT)
    except Exception as e:
        print(str(e))
