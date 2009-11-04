#!/usr/bin/python

import sys
import os
dir = os.path.dirname(sys.argv[0])
os.system(os.path.join(dir,'PsyQ')+' "'+sys.argv[1]+'"')

