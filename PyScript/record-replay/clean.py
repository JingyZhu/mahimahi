from subprocess import *
import os

mmpath = os.environ['mmpath']

call('rm -rf {}'.format(os.path.join(mmpath, 'tmp', '*')), shell=True )

call('rm plTime/*', shell=True )

call('rm RTT/*', shell=True )

call('rm network_log/*', shell=True)
