"""
    Read in each save.XXXXXX and determine whether it is cacheable
    if it is, redirect to cacheable
    else, redirect to unchacheable.
"""
import http_record_pb2
import os
from os.path import join
from subprocess import *
import tempfile
import sys
from urllib.parse import *

ip_delays = {} # Used for cache-latency
proxy_delay = 0.01
repo = join(os.environ['mmpath'], 'tmp', sys.argv[1]) if sys.argv[1] != '' else join(os.environ['mmpath'], 'tmp', 'ftp')
save_list = os.listdir(repo)
save_list = list (filter(lambda x: x[:5] == 'save.', save_list))
ips = {}
hosts_ips = {} # 'host': 'ips'
url_ttfb = {} # 'host': {'url': ttfb}

def modify_location(url, cacheable):
    # url_loc = urlparse(url)
    if cacheable:
        url = 'cacheable.' + url
        # url_loc = url_loc._replace(netloc='cacheable.'+url_loc.netloc)
    else:
        url = 'uncacheable.' + url
        # url_loc = url_loc._replace(netloc='uncacheable.'+url_loc.netloc)
    return url
    # return url_loc.geturl()

def HTTPHeader(key, value):
    http_header = http_record_pb2.HTTPHeader()
    http_header.key = key
    http_header.value = value
    return http_header


def if_cacheable(headers):
    for header in headers:
        if header.key.lower() == b'cache-control':            
            value = header.value.decode('utf-8')
            max_age = value.find('max-age')
            if max_age != -1 and 'private' not in value:
                return int(value[max_age + 8]) > 0
            return False
    return False

def get_host(headers):
    for header in headers:
        if header.key.lower() == b'host':
            return header.value.decode('utf-8')
    return None

    

def find_emptyip(ip='0.0.0.0', cacheable=False):
    for i in range(3, -1, -1):
        ip_list = ip.split('.')
        for j in range(0, 256):
            ip_list[i] = str(j)
            if '.'.join(ip_list) not in ips:
                ips['.'.join(ip_list)] = 1
                return '.'.join(ip_list)


def init_ip():
    traffic = open(join(repo, 'traffic.txt'), 'r').readlines()
    while traffic[-1] == '':
        del traffic[-1]
    for t in traffic:
        t = t.split('\t')
        ip_delays[t[0]] = float(t[1])
    for save in save_list:
        f = open(join(repo, save), 'rb').read() 
        response = http_record_pb2.RequestResponse()
        response.ParseFromString(f)
        ips[response.ip] = 1
        hosts_ips[get_host(response.request.header)] = [response.ip]
    for host, ip in hosts_ips.items():
        hosts_ips[host].append(find_emptyip(ip[0]))
        hosts_ips[host].append(find_emptyip(ip[0]))


def init_ttfb():
    ttfb = open(os.path.join(repo, 'ttfb.txt'), 'r').readlines()
    while ttfb[-1] == '':
        del ttfb[-1]
    for t in ttfb:
        parse_result = urlparse(t.split('\t')[0])
        host = parse_result.netloc
        uri = parse_result.path
        if host not in url_ttfb:
            url_ttfb[host] = {}
        url_ttfb[host][uri] = float(t.split('\t')[1])


def main():
    init_ip()
    init_ttfb()
    for save in save_list:
        f = open(join(repo, save), 'rb').read() 
        response = http_record_pb2.RequestResponse()
        response.ParseFromString(f)
        host = get_host(response.request.header)
        if host is None:
            return

        redirect = http_record_pb2.RequestResponse()
        origin = http_record_pb2.RequestResponse()
        redirect.CopyFrom(response)
        origin.CopyFrom(response)

        # Edit first line to 301, Clear others
        first_line = redirect.response.first_line.decode('utf-8').split(' ')
        first_line = [first_line[0], '301', 'Moved Permanently']
        redirect.response.first_line = ' '.join(first_line).encode('utf-8')
        redirect.response.ClearField('body')
        redirect.response.ClearField('header')

        # determine whether cacheable
        cacheable = if_cacheable(response.response.header) \
                    and response.scheme == http_record_pb2.RequestResponse.HTTP

        # Setup new host's delay and ip
        new_host = modify_location(host, cacheable)
        origin.ip = hosts_ips[host][1] if cacheable else hosts_ips[host][2]
        ip_delays[origin.ip] = proxy_delay if cacheable else ip_delays[response.ip]

        # Update hosts ttfb
        uri = urlparse(response.request.first_line.decode('utf-8').split(' ')[1]).path
        if new_host not in url_ttfb:
            url_ttfb[new_host] = {}
        if host in url_ttfb and uri in url_ttfb[host]:
            url_ttfb[new_host][uri] = url_ttfb[host][uri]
            del url_ttfb[host][uri]

        # Change host to cacheable/uncacheable
        for i in range(len(origin.request.header)):
            if origin.request.header[i].key.lower() == b'host':
                origin.request.header[i].value = new_host.encode('utf-8')

        # Set redirection location (full url)
        location = redirect.response.header.add()
        content_length = redirect.response.header.add()
        new_host += response.request.first_line.decode('utf-8').split(' ')[1]
        new_host = 'https://' + new_host if response.scheme == http_record_pb2.RequestResponse.HTTPS else 'http://' + new_host
        location.CopyFrom(HTTPHeader(b'Location', new_host.encode('utf-8') ) )
        content_length.CopyFrom(HTTPHeader(b'Content-Length', b'0'))
        
        fd2, path2 = tempfile.mkstemp('', 'save.', repo)
        # print(path1 + '\n' + path2)
        # fd0 = open(join(repo, save.replace('save', 'response')), 'w+')
        # fd1 = open(join(repo, save.replace('save', 'origin')), 'w+')
        # fd2 = open(join(repo, save.replace('save', 'redirect')), 'w+')
        fd1 = open(join(repo, save), 'wb+')
        fd1.write(redirect.SerializeToString())
        os.write(fd2, origin.SerializeToString())
        fd1.close()
        os.close(fd2)
        # print((list(response.response.header)[0]))
    traffic = open(join(repo, 'traffic.txt'), 'w+')
    for host in hosts_ips:
        ip_delays[hosts_ips[host][0]] = 0
    for ip, delay in ip_delays.items():
        traffic.write('{}\t{}\n'.format(ip, delay))
    traffic.close()
    for host, uri_delay in url_ttfb.items():
        if uri_delay == {}:
            continue
        f = open(os.path.join(repo, host), 'w+')
        for uri, delay in uri_delay.items():
            f.write('{}\t{}\n'.format(uri, delay))
        f.close()
    

    # Write ttfb to different hosts

if __name__ == '__main__':
    main()