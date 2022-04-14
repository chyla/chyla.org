Wirtualne środowisko - PyPI, venv
=================================

.. note::

  Może Ciebie również zaintersować artykuł: `Python 3 & venv </artykuly/python/python3-venv.html>`__


.. pdfobject:: /_static/files/artykuly/python/python-tutorial/Wirtualne-srodowisko-PyPI-venv.pdf


PyPI
----

**The Python Package Index** (PyPI) to repozytorium pakietów (bibliotek i programów) dla języka Python dostępne pod adresem `https://pypi.org/ <https://pypi.org/>`__.

Przykładowe narzędzia dostępne w repozytorium:

* pycodestyle - https://pypi.org/project/pycodestyle/,
* pytest - https://pypi.org/project/pytest/,
* django - https://pypi.org/project/Django/,
* flask - https://pypi.org/project/Flask/.


Częste pytanie: *Jak dodać własną bibliotekę/program do repozytorium?* Instrukcja: https://packaging.python.org/tutorials/packaging-projects/

Zarządzanie pakietami (wyszukiwanie, instalacja, aktualizacja, dezinstalacja, wypisanie listy zainstalowanych pakietów) odbywa się za pomocą, uruchamianego z konsoli, programu **pip**.

**Najważniejsze polecenie** - wyświetla dostępne polecenia i ich opis:

.. code:: text

    pip


Przykłady:

**Wyszukiwanie pakietów powiązanych z biblioteką pytest**:

.. code:: text

   pip search pytest


**Instalacja pakietu**:

.. code:: text

   pip install pytest


**Instalacja konkretnej wersji pakietu**:

.. code:: text

   pip install pytest==4.3.0


**Aktualizacja pakietu do najnowszej wersji**:

.. code:: text

   pip install --upgrade pytest


**Dezinstalacja pakietu**:

.. code:: text

   pip uninstall pytest


**Wypisanie listy zainstalowanych pakietów**:

.. code:: text

   pip list
   

Więcej informacji na temat zarządzania pakietami: https://packaging.python.org/tutorials/installing-packages/


Problemy?
^^^^^^^^^

Przykładowy problem:

    Którą wersję biblioteki zainstalować, jeśli chcę korzystać z dwóch programów w tej samej chwili, a korzystają one z tych samych bibliotek, ale w różnych wersjach? Czy różne wersje tej samej biblioteki będą ze sobą współpracować?
    
    **Program A** - Wymaga Django w wersji 2.1.
    
    **Program B** - Wymaga Django w wersji 1.11 (LTS).


venv
----

Wirtualne środowisko pozwala zarządzać pakietami bez ingerencji w systemową instalację Pythona.

Moduł venv odpowiedzialny za tworzenie wirtualnego środowiska dostarczany jest wraz z domyślną instalacją Pythona 3.7. W niektórych dystrybucjach Linuksa (np. Debian/Ubuntu) może być konieczne doinstalowanie dodatkowego pakietu zawierającego moduł venv.

**Utworzenie wirtualnego środowiska** jest możliwe za pomocą polecenia ``python -m venv``, argumentem do modułu jest nazwa środowiska (w poniższym przykładzie webenv):

.. code:: text

    python -m venv webenv

W przypadku powłoki BASH, **do aktywacji środowiska służy polecenie source.** Parametrem jest_ścieżka do skryptu, który odpowiednio zmienia zmienne środowiskowe (np. ``PATH``, ``PS1``):

.. code:: text

    source webenv/bin/activate

W przypadku powłoki systemu Windows **aktywację środowiska przeprowadza się_poprzez_uruchomienie skryptu activate**.

.. code:: text

    webenv\Scripts\activate


Do **dezaktywacji środowiska** służy polecenie:

.. code:: text

    deactivate


**Po aktywacji możemy używać poleceń związanych z pythonem**. Przyładowo, instalację Django w wersji 1.8.13 wykonujemy poleceniem:

.. code:: text

    pip install Django==1.8.13


Innymi komendami, które warto znać, są:

.. code:: text

    pip freeze > nazwa_pliku

.. code:: text

    pip install -r nazwa_pliku

Pierwsze polecenie polecenie tworzy plik, którego zawartością jest lista zainstalowanych w środowisku pakietów, wraz z ich wersjami. Ogólnie przyjęta nazwa pliku to ``requirements.txt``. Tworząc nowe, czyste środowisko możemy wczytać taką listę i zainstalować pakiety w niej zawarte (drugie polecenie).


Literatura
----------

1. `Obsługa polecenia PIP i informacje o wirtualnych środowiskach <https://packaging.python.org/tutorials/installing-packages/>`__
2. `Opis innych narzędzi do zarządania wirtualnym środowiskiem <https://docs.python-guide.org/dev/virtualenvs/>`__
