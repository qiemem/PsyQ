#!/usr/bin/env python

# A little script to convert all QT .ui files to .py files for use by PyQt4.

import os
import sys

def ui_to_py(filename):
    print("Converting "+filename)
    if os.system("pyuic4 "+filename+" > "+filename[:-3]+".py")!=0:
        print("Failed to convert "+filename)

if __name__ == '__main__':
    files = os.listdir(".")
    map(ui_to_py, filter(lambda f : f.endswith(".ui"),files))
    
