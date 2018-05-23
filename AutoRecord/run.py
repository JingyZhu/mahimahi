from subprocess import *
import os

#call(['python3', 'get_web.py'])

web_list = open('weblist', 'r').read().split('\n')
while web_list[-1] == "":
    del web_list[-1]

mmwebrecord = os.path.join(os.environ['mmpath'], 'usr/bin/mm-webrecord')
repo =  os.path.join(os.environ['mmpath'], 'tmp')
print(mmwebrecord)

for web in web_list:
    print(web + '\n')
    call([mmwebrecord, os.path.join(repo, web), 'python3', 'chrome.py', web], env=os.environ.copy())
    call(['python3', 'parse.py', os.path.join(repo, web, 'traffic.pcap')])