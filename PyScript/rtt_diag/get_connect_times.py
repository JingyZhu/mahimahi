import sys
import subprocess
from urllib.parse import urlparse
import time

if len(sys.argv) != 2:
    print('Usage: {0} [url_list]'.format(sys.argv[0]))

COMMAND = 'curl -w "@curl-format" -o /dev/null -s {0}'
PING = 'ping -c 5 {0} | grep avg'
CHROME_TCPDUMP = 'python3 chrome.py {}'

input_filename = sys.argv[1]

with open(input_filename, 'r') as input_file:
    for l in input_file:
        ip = l.split('\t')[0]
        url = l.split('\t')[1].strip()
        url_command = COMMAND.format(url)
        ping_command = PING.format(urlparse(url).netloc)
        # print(url_command)
        url_output_list = []
        try:
            for i in range(5):
                url_output = subprocess.check_output(url_command, shell=True)
                url_output_list.append(float(url_output.decode('utf-8')))
            ping_output = subprocess.check_output(ping_command, shell=True).decode('utf-8')
            ping_output = float(ping_output.split('/')[4])/1000

            chrome_tcpdump = subprocess.check_output(CHROME_TCPDUMP.format(url), shell=True).decode('utf-8')
            chrome_output = float(chrome_tcpdump.split('\t')[0])
            tcpdump_output = float(chrome_tcpdump.split('\t')[1])

            print('{}\t{}\t{}\t{}\t{}'.format(ip, sorted(url_output_list)[2], ping_output, chrome_output, tcpdump_output))
        except Exception as e:
            pass
