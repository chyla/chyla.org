Przydatne narzędzia do pracy z Pythonem
=======================================

.. contents:: Spis treści
    :backlinks: none
    :local:
    :depth: 1

pyenv
-----

Zarządzanie różnymi wersjami Pythona.

    pyenv lets you easily switch between multiple versions of Python. It's simple, unobtrusive, and follows the UNIX tradition of single-purpose tools that do one thing well.

Strona domowa: https://github.com/pyenv/pyenv


pyenv installer
^^^^^^^^^^^^^^^

Narzędzie do instalacji pyenv.

    This tool installs pyenv and friends. It is inspired by rbenv-installer.

Strona domowa: https://github.com/pyenv/pyenv-installer


Krótka instrukcja instalacji
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Pobieranie pyenv (z użyciem pyenv installer):

.. code-block:: text

    curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

2. Linie w `~/.bashrc` potrzebne do działania pyenv:

.. code-block:: text

    export PATH="$HOME/.pyenv/bin:$PATH"
    eval "$(pyenv virtualenv-init -)"
    eval "$(pyenv init -)"
    eval "$(pyenv init --path)"

3. Instalacja zależności potrzebnych do zbudowania CPythona: https://github.com/pyenv/pyenv/wiki#suggested-build-environment


virtualenv
----------

Narzędzie dla Pythona 2 i Pythona 3 do tworzenia wirtualnego środowiska.

    A tool for creating isolated virtual python environments.

PyPi: https://pypi.org/project/virtualenv/

GitHub: https://github.com/pypa/virtualenv

Dokumentacja: https://virtualenv.pypa.io/en/latest/

Wskazówki użycia: `Python - virtualenv </artykuly/python/python-virtualenv.html>`__


venv
----

Narzędzie dostarczane z Pythonem od wersji 3.3 do tworzenia wirtualnego środowiska.

    The venv module provides support for creating lightweight “virtual environments” with their own site directories, optionally isolated from system site directories. Each virtual environment has its own Python binary (which matches the version of the binary that was used to create this environment) and can have its own independent set of installed Python packages in its site directories.

Dokumentacja: https://docs.python.org/3/library/venv.html

Wskazówki użycia: `Python 3 - venv </artykuly/python/python3-venv.html>`__, `Wirtualne środowisko - PyPI, venv </artykuly/python/python-tutorial/wirtualne-srodowisko-pypi-venv.html>`__


pycodestyle (dawniej pep8)
--------------------------

Sprawdzanie stylu kodu.

    pycodestyle is a tool to check your Python code against some of the style conventions in PEP 8.


PyPi: https://pypi.org/project/pycodestyle/

GitHub: https://github.com/PyCQA/pycodestyle

Dokumentacja: https://pycodestyle.pycqa.org/en/stable/


flake8
------

Do sprawdzania stylu kodu i wyłapywania niektórych błędów.

    Flake8 is a wrapper around these tools:

    * PyFlakes
    * pycodestyle
    * Ned Batchelder's McCabe script

PyPi: https://pypi.org/project/flake8/

GitHub: https://github.com/pycqa/flake8

Dokumentacja: https://flake8.pycqa.org/en/stable/


pylint
------

Do sprawdzania stylu kodu i wyłapywania niektórych błędów.

    Pylint is a Python static code analysis tool which looks for programming errors, helps enforcing a coding standard, sniffs for code smells and offers simple refactoring suggestions.

PyPi: https://pypi.org/project/pylint/

GitHub: https://github.com/PyCQA/pylint

Dokumentacja: https://pylint.pycqa.org/en/stable/


black
-----

Formatowanie kodu.

PyPi: https://pypi.org/project/black/

GitHub: https://github.com/psf/black

Dokumentacja: https://black.readthedocs.io/en/stable/

Przydatne opcje:

* `-l <num>` - How many characters per line to allow.
* `--experimental-string-processing` (`will be enabled by default in the future <https://github.com/psf/black/issues/2188>`__) - Black splits long strings (using parentheses where appropriate) and merges short ones. When split, parts of f-strings that don’t need formatting are converted to plain strings. User-made splits are respected when they do not exceed the line length limit. Line continuation backslashes are converted into parenthesized strings. Unnecessary parentheses are stripped. Because the functionality is experimental, feedback and issue reports are highly encouraged! (`opis funkcjonalności <https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html#strings>`__)

    Black is the uncompromising Python code formatter.
