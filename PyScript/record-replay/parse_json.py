import json
import os
from os.path import join
import sys
from urllib.parse import urlparse

file = open(join('network_log', sys.argv[1]), 'r').read()
logs = json.loads(file)

for log in logs:
    if log.get('redirectResponse') != None and log['redirectResponse'].get('timing') != None:
        timing = log['redirectResponse']['timing']
        print('{}\t{}\t{}'.format(timing['requestTime'], timing['sendEnd'], urlparse(log['redirectResponse']['headers']['Location']).netloc))