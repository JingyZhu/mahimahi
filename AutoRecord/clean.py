from subprocess import *
import os

mmpath = os.environ['mmpath']

call('rm -rf {}'.format(os.path.join(mmpath, 'tmp', '*')), shell=True )

call('rm pl*/*', shell=True )

call('rm RTT/*', shell=True )
