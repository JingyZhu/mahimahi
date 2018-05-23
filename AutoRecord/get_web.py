import re

web_dict = {'google.com': 0}
webs = open('weblist_all', 'r').read().split('\n')

i = 0


for web in webs:
    web = web.split(',')
    sre = re.search('google.', web[1])
    if sre is not None and sre.start() == 0:
        continue
    web_dict[web[1]] = web[0]
    i += 1
    if i >=500:
        break

weblist = open('weblist', 'w+')
for web in web_dict:
    weblist.write(web+'\n')
weblist.close()
