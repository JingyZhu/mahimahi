from subprocess import *
import threading
import time
import sys
from queue import Queue
import os
import time

web = sys.argv[1]

sem = threading.Semaphore(0)

record = True if len(sys.argv) == 3 and sys.argv[2]=="record" else False

def run_chrome():
    Popen(['chromium-browser', '--remote-debugging-port=9222', '--ignore-certificate-errors', '--user-data-dir=/tmp/nonexistent$(date +%s%N)', '--disk-cache-size=1'])
    sem.acquire()
    # call(['pkill', 'chromium'])

chrome = threading.Thread(target=run_chrome)
chrome.start()

time.sleep(10)
begin = time.time()
call(['node', 'run.js', web])
end = time.time()

stage = 'record' if record else 'replay'
lastslash = web.rfind('/')
time_collection = open(os.path.join('plTime', web[lastslash+1:]), 'a')
time_collection.write("{}\t{}\n".format(stage, str(end-begin)))
time_collection.close()

if record:
    time.sleep(3)

sem.release()
