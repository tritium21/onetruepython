# script to register Python 2.7(!) or later for use with
# win32all and other extensions that require Python
# registry settings
#
# Adapted by Ned Batchelder and Alex Waters from a script
# written by Joakim Low for Secret Labs AB / PythonWare
#
# This code is in the public domain.
#
# http://effbot.org/zone/copyright.htm
#
# source:
# http://www.pythonware.com/products/works/articles/regpy20.htm
# http://effbot.org/zone/python-register.htm
# http://nedbatchelder.com/blog/201007/installing_python_packages_from_windows_installers_into.html

from __future__ import print_function
import argparse
import ctypes
import ctypes.wintypes
import errno
import logging
import msvcrt
import os.path
import subprocess
import sys
try:
    import winreg
except ImportError:
    import _winreg as winreg


logging.basicConfig(level=logging.INFO)

class CheckFailure(Exception):
    pass


def check_python(python):
    """
    Takes the path to something suspected to be a python executable,
    attempts to evaluate code with it (helpfully, code that gives us
    information we need anyways), and checks the output.

    Returns the version number and prefix path, raises on failure
    """
    command = "import sys; print('|'.join([sys.version[:3], sys.prefix]))"
    if not os.path.exists(python):
        raise CheckFailure("Path does not exist.")
    try:
        args = [python, '-c', command]
        out = subprocess.check_output(args).strip()
        if not isinstance(out, str):
            out  = out.decode('ascii')
        version, prefix = out.split('|')
        return version, prefix
    except subprocess.CalledProcessError:
        raise CheckFailure("Executable does not appear to be python.")


def register_python(python=sys.executable):
    """
    Does the bulk of the work.  Accepts a path to a python executable,
    and sets it as the system default python.
    """
    version, prefix = check_python(python)

    regpath = "SOFTWARE\\Python\\Pythoncore\\{0}\\".format(version)
    installkey = "InstallPath"
    pythonkey = "PythonPath"
    pythonpath = "{0};{0}\\Lib\\;{0}\\DLLs\\".format(prefix)

    try:
        reg = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, regpath)
    except EnvironmentError:
        reg = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, regpath)
    winreg.SetValue(reg, installkey, winreg.REG_SZ, prefix)
    winreg.SetValue(reg, pythonkey, winreg.REG_SZ, pythonpath)
    winreg.CloseKey(reg)
    return version, prefix


class SHELLEXECUTEINFO(ctypes.Structure):
    _fields_ = (
        ("cbSize",ctypes.wintypes.DWORD),
        ("fMask",ctypes.c_ulong),
        ("hwnd",ctypes.wintypes.HANDLE),
        ("lpVerb",ctypes.c_char_p),
        ("lpFile",ctypes.c_char_p),
        ("lpParameters",ctypes.c_char_p),
        ("lpDirectory",ctypes.c_char_p),
        ("nShow",ctypes.c_int),
        ("hInstApp",ctypes.wintypes.HINSTANCE),
        ("lpIDList",ctypes.c_void_p),
        ("lpClass",ctypes.c_char_p),
        ("hKeyClass",ctypes.wintypes.HKEY),
        ("dwHotKey",ctypes.wintypes.DWORD),
        ("hIconOrMonitor",ctypes.wintypes.HANDLE),
        ("hProcess",ctypes.wintypes.HANDLE),
    )


def need_admin():
    argv = ' '.join([os.path.abspath(__file__)] + sys.argv[1:]).strip()
    if not isinstance(argv, bytes):
        argv = argv.encode('ascii')

    if not isinstance(sys.executable, bytes):
        exe = sys.executable.encode('ascii')
    else:
        exe = sys.executable

    ShellExecuteEx = ctypes.windll.shell32.ShellExecuteEx
    ShellExecuteEx.restype = ctypes.wintypes.BOOL
    sei = SHELLEXECUTEINFO()
    sei.cbSize = ctypes.sizeof(sei)
    sei.lpVerb = b"runas"
    sei.lpFile = exe
    sei.lpParameters = argv
    sei.nShow = 1
    ShellExecuteEx(ctypes.byref(sei))


def execute(python=sys.executable):
    try:
        try:
            version, prefix = register_python(python)
            logging.info("Python %s at %s is registered!", version, prefix)
            return 0
        except WindowsError as e:
            if e.errno == errno.EACCES:
                need_admin()
            else:
                raise
    except CheckFailure as e:
        logging.exception("Unable to register: %s", e)
        return 1
    finally:
        if ctypes.windll.shell32.IsUserAnAdmin():
            # need_admin pops up a new window that disappears instantly.
            print("Press any key to continue...", end='')
            msvcrt.getch()

def main(argv=None):
    parser = argparse.ArgumentParser(description='Register the One True Python')
    parser.add_argument(
        '-p', '--python',
        default=sys.executable,
        help="The full path to the python.exe to register"
    )
    args = parser.parse_args(argv)
    return execute(args.python)


if __name__ == '__main__':
    sys.exit(main())