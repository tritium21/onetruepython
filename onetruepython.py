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
import sys

try:
    from _winreg import OpenKey, CreateKey, SetValue, CloseKey, HKEY_LOCAL_MACHINE, REG_SZ
except ImportError:
    from winreg import OpenKey, CreateKey, SetValue, CloseKey, HKEY_LOCAL_MACHINE, REG_SZ
import ctypes
import ctypes.wintypes
import os.path


def RegisterPy():
    version = sys.version[:3]
    installpath = sys.prefix

    regpath = "SOFTWARE\\Python\\Pythoncore\\{0}\\".format(version)
    installkey = "InstallPath"
    pythonkey = "PythonPath"
    pythonpath = "{0};{0}\\Lib\\;{0}\\DLLs\\".format(installpath)

    try:
        reg = OpenKey(HKEY_LOCAL_MACHINE, regpath)
    except EnvironmentError:
        reg = CreateKey(HKEY_LOCAL_MACHINE, regpath)
    SetValue(reg, installkey, REG_SZ, installpath)
    SetValue(reg, pythonkey, REG_SZ, pythonpath)
    CloseKey(reg)
    return version, installpath


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
    ShellExecuteEx = ctypes.windll.shell32.ShellExecuteEx
    ShellExecuteEx.restype = ctypes.wintypes.BOOL
    sei = SHELLEXECUTEINFO()
    sei.cbSize = ctypes.sizeof(sei)
    sei.lpVerb = b"runas"
    sei.lpFile = bytes(sys.executable, 'ascii')
    sei.lpParameters = bytes(os.path.abspath(__file__), 'ascii')
    sei.nShow = 1
    ShellExecuteEx(ctypes.byref(sei))


if __name__ == "__main__":
    try:
        try:
            res = RegisterPy()
            print("Python {0} at {1} is registered!".format(res[0], res[1]))
        except WindowsError as e:
            if e.errno == 13:
                need_admin()
            else:
                raise
    except Exception as e:
        print("Unable to register: {0}".format(e))
    finally:
        if ctypes.windll.shell32.IsUserAnAdmin():
            # need_admin pops up a new window that disappears instantly.
            input("Press any key to continue...")