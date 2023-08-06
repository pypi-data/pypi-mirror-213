.. highlight:: shell

============
Contributing
============

Python settings
---------------

fullask-rest-framework supports python 3.8 or newer.
so make it sure python3.8 or newer version is installed on your computer.

.. code-block:: console

    $ python3 --version


Git & GitHub settings
---------------------

fullask-rest-framework uses Git for its version&source control, and its Git repository is hosted on Github.
before writing your code, make sure that you installed Git on your computer.

.. code-block:: console

    $ git --version

After installing it, make yout GitHub account and fork the fullask-rest-framework's repository.
and create a local copy of your fork.

.. code-block:: console

    $ git clone https://github.com/{{ your_github_nickname }}/fullask_rest_framework.git

this will make a new directory, named "fullask_rest_framework". after cloning it, switch working directory to fullask_rest_framework.

.. code-block:: console

    $ cd fullask_rest_framework

and set up tgoddessana/fullask_rest_framework as an "upstream" remote.

.. code-block:: console

    $ git remote add upstream https://github.com/TGoddessana/fullask-rest-framework.git
    $ git fetch upstream

Python virtualenv settings
--------------------------

.. code-block:: console

    $ python3 -m venv venv

this will make virtualenv on your local computer.

and activate the virtualenv.

- windows

.. code-block:: console

    $ venv\Scripts\activate

- linux/MacOS

.. code-block:: console

    $ . venv/bin/activate

and upgrade your pip and setuptools version.

.. code-block:: console

    $ python -m pip install --upgrade pip setuptools

install the requirements for development.

.. code-block:: console

    $ pip install -r requirements_dev.txt

Python code style guide
--------------

python code of fullask_rest_framework are formatted with `black` and `isort.`


JavaScript code style guide
--------------

JavaScript code of fullask_rest_framework are formatted with `ESlint`.
