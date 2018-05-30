from subprocess import *
import os
import sys
import shutil


mmwebrecord = os.path.join(os.environ['mmpath'], 'usr/bin/mm-webrecord')
mmlink = os.path.join(os.environ['mmpath'], 'usr/bin/mm-link')

repo =  os.path.join(os.environ['mmpath'], 'tmp')
url = sys.argv[1]

web = url[url.find('www')+4:]

try:
    call([mmwebrecord, os.path.join(repo, web), mmlink, 'trace_file', 'trace_file', '--', 'python3', 'chrome.py', url, 'record'], timeout=30, env=os.environ.copy())
    shutil.copyfile('tmp', os.path.join(repo, web, 'ttfb.txt'))
    call(['python3', 'parse.py', os.path.join(repo, web)])
except Exception as e:
    print(str(e))