from subprocess import *
import os

http = 'http://'
https = 'https://'
#call(['python3', 'get_web.py'])

web_list = open('weblist', 'r').read().split('\n')
while web_list[-1] == "":
    del web_list[-1]

mmwebrecord = os.path.join(os.environ['mmpath'], 'usr/bin/mm-webrecord')
repo =  os.path.join(os.environ['mmpath'], 'tmp')

for web in web_list:
    web = web.split(',')
    print(web[0] + '\n')
    url = https + web[0] if bool(web[1]) else http + web[0]
    web = web[0]
    call([mmwebrecord, os.path.join(repo, web), 'python3', 'chrome.py', url, 'record'], env=os.environ.copy())
    call(['python3', 'parse.py', os.path.join(repo, web, 'traffic.pcap')])