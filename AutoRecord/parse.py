from scapy.all import *
import sys
import os
from ipaddress import ip_address
import subprocess
from subprocess import Popen

pkts = rdpcap(sys.argv[1])
ip_map = {} # ip: [S, SA]
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
    return (time, src, dst)

def is_private(address):
    return address.split('.')[0] == '192' and address.split('.')[1] == '168'

def ping(ip):
    print(ip)
    p = Popen(['ping', '-c', '5', ip], stdout=subprocess.PIPE)
    msg = p.communicate()[0].decode("utf-8")
    print(msg)
    rtt = msg.split('/')
    if msg == '' or len(rtt) < 7:
        return None
    return float(rtt[-3])/1000

def main():
    for pkt in pkts:
        time, src, dst = parse_pkt(pkt)
        if is_private(src) and dst not in ip_map:  # SYN msg
            ip_map[dst] = [time]
        elif is_private(dst) and len(ip_map[src]) == 1:
            ip_map[src].append(time)
    # for ip in ip_map:
    #     rtt = ping(ip)
    #     ping_map[ip] = rtt
    f = open(os.path.join(os.environ['PWD'], 'RTT', os.path.dirname(sys.argv[1]).split('/')[-1]) , 'w+')
    f2 = open(os.path.join(os.path.dirname(sys.argv[1]), 'traffic.txt'), 'w+')
    for ip, times in ip_map.items():
        if len(times) < 2:
            continue
        f.write('{}\t{}\n'.format(ip, times[1]-times[0]))
        f2.write('{}\t{}\n'.format(ip, times[1]-times[0]))
    f.close()
    f2.close()

if __name__ == '__main__':
    main()

