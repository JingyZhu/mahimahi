from subprocess import *
import os
import sys

http = 'http://www.'
https = 'https://www.'
#call(['python3', 'get_web.py'])
FNULL = open(os.devnull, 'w')
web_list = open('weblist', 'r').read().split('\n')
while web_list[-1] == "":
    del web_list[-1]

mmwebrecord = os.path.join(os.environ['mmpath'], 'usr/bin/mm-webrecord')
mmlink = os.path.join(os.environ['mmpath'], 'usr/bin/mm-link')

repo =  os.path.join(os.environ['mmpath'], 'tmp')

i = 0
for web in web_list:
    web = web.split(',')
    i += 1
    sys.stdout.flush()
    aurl = https + web[0] if bool(web[1]) else http + web[0]
    url = http + web[0]
    print(str(i) + " record: " + aurl)
    web = web[0]
    # call(['rm', '-rf', os.path.join(repo, web)])
    try:
        call([mmwebrecord, os.path.join(repo, web), mmlink, 'trace_file', 'trace_file', '--', 'python3', 'chrome.py', url, 'record'], timeout=30, env=os.environ.copy(), stdout=FNULL, stderr=STDOUT)
        call(['python3', 'parse.py', os.path.join(repo, web, 'traffic.pcap')])
    except Exception as e:
        print("Something wrong with recording {}: {}".format(web, str(e)) )
   
