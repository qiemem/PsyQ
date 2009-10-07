#! /usr/bin/env python
import os
import sys

if __name__ == '__main__':
    error = False
    try:
        pyinst_path = sys.argv[1];
    except:
        print("You must tell me where PyInstaller is.")
        sys.exit(1)
    makespec = os.path.join(pyinst_path, "Makespec.py")
    build = os.path.join(pyinst_path, "Build.py")
    if not os.path.isfile(makespec):
        print("*error* Can't find Makespec.py in "+pyinst_path)
        error = True
    if not os.path.isfile(build):
        print("*error* Can't find Build.py in "+pyinst_path)
        error = True
    if error:
        sys.exit(1)
    gen_spec = "python "+makespec+" src/start.py --onefile --name=PsyQ"
    print("Generating spec file: "+gen_spec)
    if os.system(gen_spec) != 0:
        print("*error* Makespec.py returned in error.")
        sys.exit(1)
    build_ex = "python "+build+" PsyQ.spec"
    print("Building executable: "+build_ex)
    if os.system(build_ex) != 0:
        print("*error* Build.py returned in error.")
        sys.exit(1)
    sys.exit(0)
