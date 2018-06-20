"""
    Read traffic.pcap and analyze RTT for each ip address
    Read ttfb.txt (redirected by run.js)  and analyze ttfb for each hosts and uris.
"""
from scapy.all import *
import sys
import os
from ipaddress import ip_address
import subprocess
from subprocess import Popen
from math import ceil
from urllib.parse import urlparse

repo = sys.argv[1] if sys.argv[1] != '' else 'ftp'
pkts = rdpcap(os.path.join(repo, 'traffic.pcap'))
# ttfb = open(os.path.join(repo, 'ttfb.txt'), 'r').readlines()
ip_map = {} # ip: [S, SA]
host_map = {} # host: {url: delay}
ping_map = {}

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
    return address == '10.0.2.15'# '172.31.3.103'
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


def main():
    for pkt in pkts:
        if pkt is None:
            continue
        flag, time, src, dst = parse_pkt(pkt)
        if is_private(src) and dst not in ip_map:  # SYN msg
            ip_map[dst] = [time]
        elif is_private(dst) and src in ip_map and len(ip_map[src]) == 1:  # SA msg
            ip_map[src].append(time)

    f = open(os.path.join(os.environ['PWD'], 'RTT', os.path.basename(repo)) , 'w+')
    f2 = open(os.path.join(sys.argv[1], 'traffic.txt'), 'w+')
    for ip, times in ip_map.items():
        if len(times) < 2:
            continue
        rtt = times[1] - times[0]
        f.write('{}\t{}\n'.format(ip, rtt))
        f2.write('{}\t{}\n'.format(ip, rtt))
    f.close()
    f2.close()



if __name__ == '__main__':
    main()

