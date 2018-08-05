from subprocess import *
import threading
import time
import sys
from queue import Queue
import os
import time
from scapy.all import *


device = 'ens5'
this_ip = '172.31.4.182'

web = sys.argv[1]

sem = threading.Semaphore(0)

FNULL = open('/dev/null', 'w')
TCP_COMMAND = 'sudo tcpdump -i {} tcp and port not 22 -w temp.pcap'

def run_chrome():
    Popen(['chromium-browser', '--headless', '--remote-debugging-port=9222', '--disable-gpu', '--ignore-certificate-errors', '--user-data-dir=/tmp/nonexistent$(date +%s%N)', '--disk-cache-size=1'], stdout=FNULL, stderr=STDOUT)
    sem.acquire()
    call(['pkill', 'chromium'])

def run_tcpdump():
    Popen(TCP_COMMAND.format(device), shell=True, stdout=FNULL, stderr=STDOUT)
    sem.acquire()
    time.sleep(1.5)
    call(['sudo', 'pkill', 'tcpdump'])

def parse_pkt(pkt):
    ip = pkt.getlayer(IP)
    src, dst = ip.src, ip.dst
    time = pkt.time
    flags =str(pkt['TCP'].flags)
    return (flags, time, src, dst)

def analyze_pcap(pcap):
    ip_map = {}
    pkts = rdpcap('temp.pcap')
    for pkt in pkts:
        if pkt is None:
            continue
        flag, time, src, dst = parse_pkt(pkt)
        if src == this_ip and dst not in ip_map:  # SYN msg
            ip_map[dst] = [time]
        elif dst == this_ip and src in ip_map and len(ip_map[src]) == 1:  # SA msg
            ip_map[src].append(time)
            break
    for ip, rtts in ip_map.items():
        if len(rtts) > 1:
            return (ip, float(rtts[1] - rtts[0]))


chrome = threading.Thread(target=run_chrome)
tcpdump = threading.Thread(target=run_tcpdump)
tcpdump.start()
chrome.start()

time.sleep(1)
output = check_output(['node', 'run.js', web])
output = output.decode('utf-8')

ip = output.split('\t')[0]
rtt = float(output.split('\t')[1])/1000

sem.release()
sem.release()

time.sleep(2)

tcpdump_ip, tcpdump_rtt = analyze_pcap('temp.pcap')

print('{}\t{}'.format(rtt, tcpdump_rtt))