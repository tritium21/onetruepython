from __future__ import print_function
import subprocess

PYTHONS = (r"C:\python27\python.exe", r"c:\python34\python.exe")


command = "import sys; print('|'.join([sys.version[:3], sys.prefix]))"

for python in PYTHONS:
    args = [python, '-c', command]
    out = subprocess.check_output(args)
    ver, prefix = out.split('|')
    print("Path: ", python)
    print("Version: ", ver)
    print("Prefix: ", prefix)
