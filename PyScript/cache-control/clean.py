from subprocess import *
import os

call('rm -rf {}'.format(os.path.join('tmp', '*')), shell=True )

call('rm counts/*', shell=True )

call('rm bytes/*', shell=True )