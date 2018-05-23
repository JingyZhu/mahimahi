from subprocess import *
import threading
import time
import sys
from queue import Queue
import os
import time

web = "https://www." + sys.argv[1]

sem = threading.Semaphore(0)

def run_chrome():
    Popen(['chromium-browser', '--headless', '--remote-debugging-port=9222', '--disable-gpu', '--ignore-certificate-errors', '--user-data-dir=/tmp/nonexistent$(date +%s%N)'])
    sem.acquire()
    call(['pkill', 'chromium'])

chrome = threading.Thread(target=run_chrome)
chrome.start()

time.sleep(2)

print(web)
begin = time.time()
call(['node', 'run.js', web])
end = time.time()

print("Takes: " + str(end-begin))
sem.release()
