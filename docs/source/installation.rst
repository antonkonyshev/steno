Installation
************

Application dependencies
========================

The application has the following dependencies:

* wxPython
* pysrt
* google_translate_api

Installation using ``pip`` or ``easy_install``
==============================================

You can install the application using ``pip``:

::

    pip install steno

or ``easy_install``:

::

    easy_install steno

Installation from repository
============================

You can install the application using ``setuptools``:

::

    git clone git://github.com/antonkonyshev/steno.git && cd steno
    python setup.py install
    
Linux users can use ``make``:

::

    make install

Running without installation
============================

In order to run the application without installation, use the following command:

::

    python steno/steno.py
    
Linux users can use ``make``:

::

    make start
    
Compiling of a binary build
===========================

If you want to use the application on another computer, where
Python and application dependencies are not installed, you can compile
a binary build using PyInstaller.

On Linux:

::

    make build

Under Windows:

::

    set PYTHONPATH=.
    pyi-build pyi/steno.spec
    
The result will be stored in ``dist/steno.exe`` or ``dist/steno.bin``.

Unit tests running
==================

On Linux:

::

    make test
    
Under Windows:

::

    set PYTHONPATH=steno
    python -m unittest discover -v -s steno