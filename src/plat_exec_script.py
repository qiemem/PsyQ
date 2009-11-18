#!/usr/bin/python

import sys
import os
dir = os.path.dirname(sys.argv[0])
if len(sys.argv)>1:
	os.system(os.path.join(dir,'PsyQ')+' "'+sys.argv[1]+'"')
else:
	os.system(os.path.join(dir,'PsyQ'))

