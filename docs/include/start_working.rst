Start Working
-------------

.. note::

 ``python 3.6`` as least, and ``git`` are required.

Install mathmakerlib in dev mode in a venv:

* Linux

  ::

      $ cd to/your/dev/directory/
      $ python3 -m venv dev0
      $ source dev0/bin/activate
      (dev0) $ pip3 install pytest tox flake8 pydocstyle sphinx sphinx-autodoc-annotation sphinx-rtd-theme
      (dev0) $ mkdir mathmakerlib
      (dev0) $ cd mathmakerlib/
      (dev0) $ git clone https://gitlab.com/nicolas.hainaux/mathmakerlib.git
      (dev0) $ python3 setup.py develop


* FreeBSD

  ::

      $ cd to/your/dev/directory/
      $ python3 -m venv dev0
      $ source dev0/bin/activate.csh
      [dev0] $ sudo pip3 install pytest tox flake8 pydocstyle sphinx sphinx-autodoc-annotation sphinx-rtd-theme
      [dev0] $ mkdir mathmakerlib
      [dev0] $ cd mathmakerlib/
      [dev0] $ git clone https://gitlab.com/nicolas.hainaux/mathmakerlib.git
      [dev0] $ python3 setup.py develop


* Windows (PowerShell)

  It is strongly advised to develop on a Linux or FreeBSD box.
  Nevertheless, for testing purposes at least, this is useful to know how to start a virtual environment on Windows (PowerShell), so here it is:

  First open a PowerShell:
  Windows 7: start menu > search for "PowerShell" > right-click > run as administrator.
  Windows 10: hit the Windows key + X to open a PowerShell with admin rights.

  ::

    PS C:\Windows\system32> cd ../..
    PS C:\> cd .\Users\username\
    PS C:\Users\username> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
    ...
    PS C:\Users\username\venv> & 'C:\Program Files\Python36\python.exe' -m venv dev0
    PS C:\Users\username\venv> .\dev0\Scripts\Activate.ps1
    (dev0) PS C:\Users\username\venv>

  then follow the same steps as under Linux or FreeBSD: pip install the dependencies, clone the git repo and run ``setup.py`` with develop option.

  Or, if this is just for testing: ``pip install mathmakerlib``

The tests are stored under ``tests/``.

Run the tests:

::

    (dev0) $ pytest -x -vv -r w tests/

So far, more details can be found in the `documentation for developers of mathmaker <http://mathmaker.readthedocs.io/en/dev/dev_index.html>`__.
