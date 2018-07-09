"""
    Generate time charts for the log
"""

import sys

beginTime = 0
id_load = {}
id_url = {}
file = sys.argv[1]
f = open(file, 'r').readlines()

del f[-1]

for line in f:
    line =line.split('\t')
    Sent = True if line[0] == 'Sent' else False
    reqId = line[1]
    url = line[2]
    if beginTime == 0:
        beginTime = float(line[3])
    time = float(line[3]) - beginTime
    if Sent:
        id_load[reqId] = [time]
        id_url[reqId] = url
    else:
        id_load[reqId].append(time)

id_load = sorted(id_load.items(), key=lambda item: item[1][0])
strr = ""
for reqId, times in id_load:
    if len(times) > 1:
        strr += "['{}', new Date(0, 0, 0, 0, 0, 0, {}), new Date(0, 0, 0, 0, 0, 0, {})],\n".format(id_url[reqId]+str(reqId), int(times[0]*1000), int(times[1]*1000))

strr += "['dummy', new Date(0, 0, 0, 0, 0, 0), new Date(0, 0, 0, 0, 0, 0)]"

print(strr)