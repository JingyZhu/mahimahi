from subprocess import *
import os
import sys
import shutil
from urllib.parse import urlparse


mmwebrecord = os.path.join(os.environ['mmpath'], 'usr/bin/mm-webrecord')
mmlink = os.path.join(os.environ['mmpath'], 'usr/bin/mm-link')

repo =  os.path.join(os.environ['mmpath'], 'tmp')
url = sys.argv[1]

web = urlparse(url).netloc if urlparse(url).netloc!='' else 'ftp'

try:
    call([mmwebrecord, os.path.join(repo, web), mmlink, 'trace_file', 'trace_file', '--', 'python3', 'chrome.py', url, 'record'], timeout=60, env=os.environ.copy())
    shutil.copyfile('tmp', os.path.join(repo, web, 'ttfb.txt'))
    call(['python3', 'parse.py', os.path.join(repo, web)])
    call(['python3', 'transfer.py', web])
except Exception as e:
    print(str(e))