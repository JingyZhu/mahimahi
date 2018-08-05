"""
Get random website from top million websites
"""
import re
import random
import requests

web_dict = {}
inweb_dict = {}
webs = open('weblist_all', 'r').readlines()
weblist = open('weblist', 'r').readlines()
random.shuffle(webs)

for inweb in weblist:
    inweb = inweb.strip()
    inweb_dict[inweb.split(',')[0]] = inweb.split(',')[1]=='True'

i = len(inweb_dict)

for web in webs:
    web = web.strip()
    web = web.split(',')
    sre = re.search('google.', web[1])
    if web[1] in inweb_dict:
        continue
    if sre is not None and sre.start() == 0:
        continue
    web_dict[web[1]] = (web[2] == 'True')
    i += 1
    if i >=100:
        break

weblist = open('weblist2', 'w+')
for web in web_dict:
    weblist.write('{},{}\n'.format(web, web_dict[web]))
weblist.close()
