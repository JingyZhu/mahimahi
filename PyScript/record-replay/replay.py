from subprocess import *
import os
import sys
from urllib.parse import urlparse

url = sys.argv[1]
web =  urlparse(url).netloc if urlparse(url).netloc!='' else 'ftp'

mmwebreplay = os.path.join(os.environ['mmpath'], 'usr/bin/mm-webreplay')
mmlink = os.path.join(os.environ['mmpath'], 'usr/bin/mm-link')
mmdelay = os.path.join(os.environ['mmpath'], 'usr/bin/mm-delay')
repo =  os.path.join(os.environ['mmpath'], 'tmp')

try:
    call([mmwebreplay, os.path.join(repo, web), mmdelay, '170', os.path.join(repo, web), '--', 'python3', 'chrome.py', url], timeout=60, env=os.environ.copy())
except Exception as e:
    print(str(e))
