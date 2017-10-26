Start Working
-------------

.. note::

 ``python 3.6`` as least, and ``git`` are required.

Install mathmakerlib in dev mode in a venv:

* Linux::

    $ cd to/your/dev/directory/
    $ python3 -m venv dev0
    $ source dev0/bin/activate
    (dev0) $ pip3 install pytest tox flake8 pydocstyle sphinx sphinx-autodoc-annotation sphinx-rtd-theme
    (dev0) $ mkdir mathmakerlib
    (dev0) $ cd mathmakerlib/
    (dev0) $ git clone https://github.com/nicolashainaux/mathmakerlib.git
    (dev0) $ python3 setup.py develop


* FreeBSD::

    $ cd to/your/dev/directory/
    $ python3 -m venv dev0
    $ source dev0/bin/activate.csh
    [dev0] $ sudo pip3 install pytest tox flake8 pydocstyle sphinx sphinx-autodoc-annotation sphinx-rtd-theme
    [dev0] $ mkdir mathmaker
    [dev0] $ cd mathmaker/
    [dev0] $ git clone https://github.com/nicolashainaux/mathmakerlib.git
    [dev0] $ python3 setup.py develop

Here's how to start a virtual environment on Windows 10 PowerShell: hit the Windows key + X to open a PowerShell with admin rights, then:

* Windows 10::

    PS C:\Windows\system32> cd ../..
    PS C:\> cd .\Users\username\
    PS C:\Users\username> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
    ...
    PS C:\Users\username\venv> & 'C:\Program Files\Python36\python.exe' -m venv dev0
    PS C:\Users\username\venv> .\dev0\Scripts\Activate.ps1
    (dev0) PS C:\Users\username\venv>

then pip install the dependencies, clone the git repo and run ``setup.py`` with develop option.



The tests are stored under ``tests/``.

Run the tests:
::

    (dev0) $ py.test

So far, more details can be found in the `documentation for developers of mathmaker <http://mathmakerlib.readthedocs.io/en/dev/dev_index.html>`__.
