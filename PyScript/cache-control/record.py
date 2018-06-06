from subprocess import *
import os
import sys

http = 'http://www.'
https = 'https://www.'

FNULL = open(os.devnull, 'w')

web_list = open('weblist', 'r').read().split('\n')
while web_list[-1] == "":
    del web_list[-1]

i = 0
for web in web_list:
    web = web.split(',')
    i += 1
    sys.stdout.flush()
    url = https + web[0] if web[1] == 'True' else http + web[0]
    print(str(i) + ". " + url)
    web = web[0]
    # call(['rm', '-rf', os.path.join(repo, web)])
    try:
        filename = os.path.join('tmp', web)
        webfile = open(filename, 'w+')
        call(['python3', 'chrome.py', url, 'record'], timeout=120, env=os.environ.copy(), stdout=webfile, stderr=FNULL)
        call(['python3', 'bytes.py', web])
        call(['python3', 'count.py', web])
        webfile.close()
    except Exception as e:
        print("Something wrong with recording {}: {}".format(web, str(e)) )
