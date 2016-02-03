from __future__ import print_function
import subprocess
import os.path

PYTHONS = (r"C:\python27\python.exe", r"c:\python34\python.exe")


command = "import sys; print('|'.join([sys.version[:3], sys.prefix]))"

for python in PYTHONS:
    pass


def check_version_prefix(python):
    try:
        args = [python, '-c', command]
        out = subprocess.check_output(args)
        ver, prefix = out.split('|')
        return ver, prefix
    except subprocess.CalledProcessError:
        return False


def check_lib(python):
    pydir = os.path.basename(os.path.abspath(python))
    if os.path.basename(pydir).lower() != 'scripts':
        return
    libdir = os.path.join(os.path.basename(pydir), 'Lib')
    if not os.path.isdir(libdir):
        return
    return pydir, libdir
