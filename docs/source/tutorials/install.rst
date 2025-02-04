Installation
============

Install Python
--------------

Being a Python library, MetPyRad requires `Python <https://www.python.org/>`_,
so you need to install the Python 3 interpreter on your computer.
You can get the latest version of Python at the official `Python downloads site <https://www.python.org/downloads/>`_
or with your operating system’s package manager.
The Python documentation also has a `detailed installation guide <https://docs.python.org/3/using/index.html>`_
on how to install and setup Python.

You can verify that Python is installed by running the following command in your shell prompt:

.. code-block:: console

    $ python --version

You should see an output like:

.. code-block:: console

    Python 3.12.3

Set up a virtual environment
----------------------------

The recommended way to install packages not included in the standard library is using
`virtual environments <https://docs.python.org/3/library/venv.html>`_.
Python virtual environments allow you to keep a separate directory of installed packages for each of your projects
so that they don’t interfere with each other.
It is not recommended to install packages system-wide.
The Python documentation also has a `detailed tutorial <https://docs.python.org/3/tutorial/venv.html>`_
on how to create and use virtual environments.

Once you have created and activated your virtual environment, its name is displayed on the command line
so that you can see which one you are using.
Common names used for virtual environments are ``venv`` or ``.venv``.
You should see something like:

.. code-block:: console

    (venv)$

Install MetPyRad
----------------

The recommended way to install MetPyRad is using the
`package installer for Python (pip) <https://docs.python.org/3/installing/index.html>`_.
MetPyRad can be installed from the `Python Package Index (PyPI) <https://pypi.org/project/metpyrad/>`_
by running the following command in your shell prompt:

.. code-block:: console

    $ pip install metpyrad

You can verify that Python is installed by running the following command in your shell prompt:

.. code-block:: console

    $ pip freeze | grep metpyrad

You should see something like:

.. code-block:: console

    metpyrad==0.0.1
