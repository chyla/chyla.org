Python & virtualenv
===================

.. note::

    Może Ciebie również zaintersować artykuł: `Python 3 & venv </artykuly/python/python3-venv.html>`__


Wirtualne środowisko pozwala zarządzać pakietami bez ingerencji w systemową instalację Pythona.

`virtualenv <https://github.com/pypa/virtualenv>`__ jest narzędziem dodatkowym, nie jest dostarczany razem z interpreterem (Python 3 dostarcza moduł venv, o którym przeczytasz `tutaj </artykuly/python/python3-venv.html>`__).


Instalacja virtualenv jest dość prosta i sprowadza się do wydania polecenia:

.. code-block:: text

    pip install virtualenv

Prawdopodobnie, oprogramowanie znajduje się także w repozytorium Twojej dystrybucji Linuksa - w Debianie (i dystrybucjach Debiano-pochodnych) jest to pakiet ``python-virtualenv``.


Utworzenie wirtualnego środowiska jest możliwe za pomocą polecenia virtualenv, argumentem do programu jest nazwa środowiska (w poniższym przykładzie webenv):

.. code-block:: text

    virtualenv webenv

Wybrany zostanie domyślny interpreter Pythona, aby to zmienić można użyć przełącznika `-p` i wskazać konkretny interpreter (dokładna ścieżka zależy od Twojego systemu operacyjnego i interpretera):

.. code-block:: text

    virtualenv -p /usr/bin/python2 webenv

.. code-block:: text

    virtualenv -p /usr/bin/python3 webenv


Do aktywacji środowiska w ystemie Linux służy polecenie `source <https://en.wikipedia.org/wiki/Source_(command)>`__. Parametrem jest ścieżka do skryptu, który odpowiednio zmienia zmienne środowiskowe (np. PATH, PS1):

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

Pierwsze polecenie polecenie tworzy plik, którego zawartością jest lista zainstalowanych w środowisku pakietów, wraz z ich wersjami. Często taki plik nosi nazwę ``requirements.txt``, a `tutaj jego przykład <https://github.com/chyla/pat-lms/blob/fb5ac20ac75c08ea11933133dc3675136b50ee28/web/requirements.txt>`__. Tworząc nowe, czyste środowisko możemy wczytać taką listę i zainstalować pakiety w niej zawarte (drugie polecenie).

Dezaktywacji wirtualnego środowiska dokonujemy za pomocą polecenia:

.. code-block:: text

    deactivate

    
Poniżej literatura, w której znajdziesz więcej informacji na temat *virtualenv*. Ciekawym rozwiązaniem jest *virtualenvwrapper*, którego tutaj nie przedstawiłem, gdyż jest to tylko 'nakładka' na polecenia virtualenv.


Literatura
----------

1. `Virtualenv <https://github.com/pypa/virtualenv>`__
2. `Virtualenv - Dokumentacja <https://virtualenv.pypa.io/en/latest/>`__
3. `Virtual Environments <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`__
