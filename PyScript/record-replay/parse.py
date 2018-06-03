from scapy.all import *
import sys
import os
from ipaddress import ip_address
import subprocess
from subprocess import Popen
from math import ceil
from urllib.parse import urlparse

repo = sys.argv[1]
pkts = rdpcap(os.path.join(repo, 'traffic.pcap'))
ttfb = open(os.path.join(repo, 'ttfb.txt'), 'r').read().split('\n')
ip_map = {} # ip: [S, SA]
host_map = {} # host: {url: delay}
ping_map = {}
ip_conversation_time = {}
max_step = 0.4
step = 0.025
base = 1 - max_step - step

def sec_to_datetime(sec):
    _, sec = divmod(sec, 24 * 3600)
    hour, sec = divmod(sec, 3600)
    minute, sec = divmod(sec, 60)
    second, sec = divmod(sec, 60)
    return '{}:{}:{}'.format(hour-4, minute, second)

def parse_pkt(pkt):
    ip = pkt.getlayer(IP)
    src, dst = ip.src, ip.dst
    time = pkt.time
    flags =str(pkt['TCP'].flags)
    return (flags, time, src, dst)

def is_private(address):
    return address == '172.31.3.103'
    # return address.split('.')[0] == '10' and address.split('.')[1] == '0'

def ping(ip):
    print(ip)
    p = Popen(['ping', '-c', '5', ip], stdout=subprocess.PIPE)
    msg = p.communicate()[0].decode("utf-8")
    print(msg)
    rtt = msg.split('/')
    if msg == '' or len(rtt) < 7:
        return None
    return float(rtt[-3])/1000

def max(a, b):
    if a > b:
        return a
    return b

def min(a, b):
    if a > b:
        return b
    return a

def coef_calc(times, rtt):
    return (times + max(1 , times / max(1, ceil(rtt/0.05)))) / 2

def main():
    for pkt in pkts:
        if pkt is None:
            continue
        flag, time, src, dst = parse_pkt(pkt)
        if is_private(src) and dst not in ip_map:  # SYN msg
            ip_map[dst] = [time]
            ip_conversation_time[dst] = [base, 1]
        elif is_private(dst) and src in ip_map and len(ip_map[src]) == 1:
            ip_map[src].append(time)
        if dst in ip_conversation_time and flag == 'S':
            ip_conversation_time[dst][0] += max(0, (1 - base + step) - step * ip_conversation_time[dst][1])
            ip_conversation_time[dst][1] += 1
    # for ip in ip_map:
    #     rtt = ping(ip)
    #     ping_map[ip] = rtt
    f = open(os.path.join(os.environ['PWD'], 'RTT', sys.argv[1].split('/')[-1]) , 'w+')
    f2 = open(os.path.join(sys.argv[1], 'traffic.txt'), 'w+')
    for ip, times in ip_map.items():
        if len(times) < 2:
            continue
        rtt = times[1] - times[0]
        f.write('{}\t{}\t{}\n'.format(ip, rtt, ip_conversation_time[ip][1]))
        f2.write('{}\t{}\t{}\n'.format(ip, rtt, ip_conversation_time[ip][1], rtt ))
    f.close()
    f2.close()
    while ttfb[-1] == '':
        del ttfb[-1]
    for t in ttfb:
        parse_result = urlparse(t.split('\t')[0])
        host = parse_result.netloc
        uri = parse_result.path
        if host not in host_map:
            host_map[host] = {}
        host_map[host][uri] = t.split('\t')[1]
    for host, uri_delay in host_map.items():
        f = open(os.path.join(repo, host), 'w+')
        for uri, delay in uri_delay.items():
            f.write('{}\t{}\n'.format(uri, delay))
        f.close()



if __name__ == '__main__':
    main()

