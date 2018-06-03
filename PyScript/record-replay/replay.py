from subprocess import *
import os
import sys

url = sys.argv[1]
web = url[url.find('www')+4:]

mmwebreplay = os.path.join(os.environ['mmpath'], 'usr/bin/mm-webreplay')
mmlink = os.path.join(os.environ['mmpath'], 'usr/bin/mm-link')
repo =  os.path.join(os.environ['mmpath'], 'tmp')

try:
    call([mmwebreplay, os.path.join(repo, web), mmlink, 'trace_file', 'trace_file', '--', 'python3', 'chrome.py', url], timeout=30, env=os.environ.copy())
except Exception as e:
    print(str(e))