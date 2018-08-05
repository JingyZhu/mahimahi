import os
from os.path import join
mmpath = os.environ['mmpath']

ip_rtt = {}

webs = os.listdir('RTT')


for dirr in webs:
    dirr = dirr.split(',')[0]
    traffic = open(join('RTT', dirr), 'r').readlines()
    for ip_delays in traffic:
        ip_delays = ip_delays.strip('\n').split('\t')
        ip = ip_delays[0]
        delay = float(ip_delays[1])*1000
        if ip not in ip_rtt:
            ip_rtt[ip] = delay

rtts = list(ip_rtt.values())
rtts.sort()

for i in range(len(rtts)):
    print('[{}, {}],'.format(rtts[i], (i+1)/len(rtts)))
