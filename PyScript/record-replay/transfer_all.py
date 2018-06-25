from subprocess import *
import os
from os.path import join
import sys
import shutil

mmpath = os.environ['mmpath']
web_list = open('weblist', 'r').read().split('\n')
while web_list[-1] == "":
    del web_list[-1]

for web in web_list:
    web = web.split(',')[0]
    call(['python3', 'transfer.py', web])
