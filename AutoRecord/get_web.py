import re
import random
import requests

web_dict = {'https://www.google.com': 0}
webs = open('weblist_all', 'r').read().split('\n')

random.shuffle(webs)

i = 0

for web in webs:
    web = web.split(',')
    sre = re.search('google.', web[1])
    if sre is not None and sre.start() == 0:
        continue
    web_dict[web[1]] = (web[0], bool(web[2]))
    i += 1
    if i >=100:
        break

weblist = open('weblist', 'w+')
for web in web_dict:
    weblist.write('{},{}\n'.format(web, web_dict[web][1]))
weblist.close()
