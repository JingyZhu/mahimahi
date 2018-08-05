import os
from os.path import join
from subprocess import *
import http_record_pb2
from urllib.parse import *


mmpath = os.environ['mmpath']
webs = os.listdir(join(mmpath, 'tmp'))

http = 'http://'
https = 'https://'

wanted = ['.js', '.css', '.html']
ip_uri = {}

def get_host(headers):
    for header in headers:
        if header.key.lower() == b'host':
            return header.value.decode('utf-8')
    return None

for web in webs:
    if web[-1] == '2':
        continue
    saves = os.listdir(join(mmpath, 'tmp', web))
    for save in saves:
        if save.find('save') != 0:
            continue
        protostr = open(join(mmpath, 'tmp', web, save), 'rb').read()
        response = http_record_pb2.RequestResponse()
        response.ParseFromString(protostr)
        ishttps = response.Scheme == http_record_pb2.RequestResponse.HTTPS
        ip = response.ip
        uri = response.request.first_line.decode().split(' ')[1]
        uri = urlparse(uri).path
        base_uri = os.path.basename(urlparse(uri).path)
        uri = https + get_host(response.request.header) + uri
        if ip not in ip_uri:
            ip_uri[ip] = []
        for want in wanted:
            if want in base_uri:
                ip_uri[ip].append(uri)
                break

del_ip = []
for ip in ip_uri:
    if len(ip_uri[ip]) > 0:
        ip_uri[ip] = ip_uri[ip][0]
    else:
        del_ip.append(ip)

for ip in del_ip:
    del ip_uri[ip]
# print(ip_uri)
strr = ""
for ip, uri in ip_uri.items():
    strr += '{}\t{}\n'.format(ip, uri)

print(strr)

