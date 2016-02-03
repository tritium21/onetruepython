OneTruePython
=============

Some Windows installers for Python modules check for the currently installed Python
in the Windows registry.  This is all fine and good until you have more than one
Python of the same version or use virtualenvs.  At that point, the installer will
try and install the module in the last Python you installed, and often will not give
you a choice to overide that.

**OneTruePython** fixes that.

To use **OneTruePython**, download ``onetruepython.py`` and run it with the desired
``python.exe``.  If this is a new concept to you, here is how you can do that.

* Download ``onetruepython.py``, preferably to your user directory
  (``C:\Users\<your_user_name>``).  There is no need to checkout this repository, or
  use the Visual Studio solution.  All you need is that one file

* Find the ``python.exe`` of your Environment.  In a virtualenv, that would be in
  ``<ENV>\Scripts\python.exe``.  For Anaconda it would be something like
  ``C:\Anaconda2\python.exe``

* Launch a command prompt (WinKey+R, type ``cmd``, and hit enter)

* Change directories to the one with ``onetruepython.py`` (if you downloaded it to your
  user directory, like ``C:\Users\<your_user_name>\onetruepython.py``, then you wont
  need to do this, the command prompt starts there.)

* Type the path to your `python.exe` followed by `onetruepython.py`.  (Example:
  ``C:\Anaconda2\python.exe onetruepython.py``, or for virtualenvs
  ``C:\<path_to_venv>\Scripts\python.exe onetruepython.py``)

* It should ask you to elevate to an admin user.  This is expected.  If it does not
  ask you to do this, you were already running as an admin or your user account cannot
  be elevated.  In the latter case, get someone with admin privledges to run the script
  for you.

* If you are asked to elevate, a new window will open up.  That window will either tell
  you it worked, or tell you the error that happened.  If you were not asked to elevate,
  then this will happen in the command prompt you just opened.

* Thats it!  Go ahead and install that module, and it should see the right Python!