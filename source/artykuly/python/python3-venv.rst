Python 3 & venv
===============

.. note::

  Mogą Ciebie również zaintersować artykuły:

  * `Python & virtualenv </artykuly/python/python-virtualenv.html>`__
  * `Wirtualne środowisko - PyPI, venv </artykuly/python/python-tutorial/wirtualne-srodowisko-pypi-venv.html>`__


Wirtualne środowisko pozwala zarządzać pakietami bez ingerencji w systemową instalację Pythona.

Moduł `venv` odpowiedzialny za tworzenie wirtualnego środowiska **dostarczany jest wraz z domyślną instalacją od Pythona 3.3**. Przeczytaj `artykuł o virtualenv </artykuly/python/python-virtualenv.html>`__, jeśli szukasz uniwersalnego rozwiązania do wykorzystania z Pythonem 2 oraz 3.

W niektórych dystrybucjach Linuksa (np. Debian/Ubuntu) może być konieczne doinstalowanie dodatkowego pakietu zawierającego moduł `venv`.

Polecenie dla dystrybucji Debian/Ubuntu instalujące moduł `venv`:

.. code-block:: text

    sudo apt-get install python3-venv


Utworzenie wirtualnego środowiska jest możliwe za pomocą polecenia `python -m venv`, argumentem do modułu jest nazwa środowiska (w poniższym przykładzie webenv):

.. code-block:: text

    python -m venv webenv


Do aktywacji środowiska w systemie Linux służy polecenie `source <https://en.wikipedia.org/wiki/Source_(command)>`__. Parametrem jest ścieżka do skryptu, który odpowiednio zmienia zmienne środowiskowe (np. PATH, PS1):

.. code-block:: text

    source webenv/bin/activate


Po aktywacji możemy używać poleceń związanych z pythonem. Przyładowo, instalację Django w wersji 1.8.13 wykonujemy poleceniem:

.. code-block:: text

    pip install Django==1.8.13


Innymi komendami, które warto znać, są:

.. code-block:: text

    pip freeze > nazwa_pliku

oraz:

.. code-block:: text

    pip install -r nazwa_pliku

Pierwsze polecenie polecenie tworzy plik, którego zawartością jest lista zainstalowanych w środowisku pakietów, wraz z ich wersjami. Często taki plik nosi nazwę ``requirements.txt``, a `tutaj jego przykład <https://github.com/chyla/WeatherForecastAppTemplate/blob/master/requirements.txt>`__. Tworząc nowe, czyste środowisko możemy wczytać taką listę i zainstalować pakiety w niej zawarte (drugie polecenie).


Dezaktywacji wirtualnego środowiska dokonujemy za pomocą polecenia:

.. code-block:: text

    deactivate


Literatura
----------

1. `venv — Creation of virtual environments <https://docs.python.org/3/library/venv.html>`__
2. `Virtual Environments <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`__
