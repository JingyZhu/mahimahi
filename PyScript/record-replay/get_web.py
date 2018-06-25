"""
Get random website from top million websites
"""
import re
import random
import requests

web_dict = {'google.com': True}
webs = open('weblist_all', 'r').read().split('\n')
webs = webs[:500]
random.shuffle(webs)

i = 0

for web in webs:
    web = web.split(',')
    sre = re.search('google.', web[1])
    if sre is not None and sre.start() == 0:
        continue
    web_dict[web[1]] = (web[2] == 'True')
    i += 1
    if i >=50:
        break

weblist = open('weblist2', 'w+')
for web in web_dict:
    weblist.write('{},{}\n'.format(web, web_dict[web]))
weblist.close()
