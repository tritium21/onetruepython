OneTruePython
=============

Some Windows installers for Python modules check for the currently installed Python
in the Windows registry.  This is all fine and good until you have more than one
Python of the same version or use virtualenvs.  At that point, the installer will
try and install the module in the last Python you installed, and often will not give
you a choice to overide that.

**OneTruePython** fixes that.

Run onetruepython.py with the python environment (Anaconda, virtualenvs, etc), and 
it will set the registry keys to that python.  It needs to be run in an elevated
command prompt, but it will take care of starting that prompt for you.
