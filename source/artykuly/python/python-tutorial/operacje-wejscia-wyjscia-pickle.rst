Operacje wejścia/wyjścia - Pickle
=================================


.. pdfobject:: /_static/files/artykuly/python/python-tutorial/Operacje-wejscia-wyjscia-Pickle.pdf


Pickle
------

Moduł **pickle** pozwala na serializację i deserializację obiektów Pythona.

Serializacją (inaczej *marshalling*, *pickling* lub *flattening*) to proces przekształcania obiektu w ciąg bajtów. Deserializacja (inaczej *demarshalling* lub *unpicking*) to proces przeciwny -  zamiana kolejnych bajtów na obiekt.  [#pickle]_

Uzyskany w ten sposób ciąg bajtów można zapisać do pliku lub przesłać przez sieć. Dane zapisane w pliku mogą później posłużyć do odtworzenia stanu programu przy jego kolejnym uruchomieniu.


.. [#pickle] źródło: https://docs.python.org/3/library/pickle.html


.. warning::

    Za pomocą modułu pickle należy deserializować dane pochodzące wyłącznie z zaufanego źródła.

    Deserializacja niezaufanych danych może wiązać się z poważnym zagrożeniem bezpieczeństwa dla systemu, na którym działa nasz program.

    Proces deserializacji danych umożliwia wykonanie dowolnego kodu. Kontrola danych przeznaczonych do deserializacji za pomocą modułu pickle to silny atut w rękach atakującego.



Serializacja danych
-------------------

Funkcja ``dumps()`` pozwala na serializację obiektu do ciągu bajtów.

Ciąg bajtów można zapisać do pliku lub przesłać przez sieć.


.. code-block:: python

    import pickle

    phone_book = {"Jonna": "542124",
                "Maciej": "542323",
                }

    bytes = pickle.dumps(phone_book)


Zapisywanie danych do pliku
---------------------------

Zapisanie danych do pliku możemy zrealizować za pomocą funkcji ``dump()``.

Plik, w którym chcemy zapisać dane, musi zostać otworzony w trybie binarnym. Należy również pamiętać o jego zamknięciu.


.. code-block:: python

    import pickle

    phone_book = {"Jonna": "542124",
                "Maciej": "542323",
                }

    with open('app_data.pickle', 'wb') as file:
        pickle.dump(phone_book, file)


Deserializacja danych
---------------------

Funkcja ``loads()`` pozwala zamienić ciąg bajtów na obiekt.


.. code-block:: python

    import pickle

    bytes = ( b'(dp0\nVJonna\np1\nV542124\np2\nsVMaciej\np3\nV542323\np4\ns.'
    )

    phone_book = pickle.loads(bytes)


Wczytywanie danych z pliku
--------------------------

Odczyt danych z pliku możemy zrealizować za pomocą funkcji ``load()``.

Plik, z którego chcemy odczytać dane, musi zostać otworzony w trybie binarnym. Należy również pamiętać o jego zamknięciu.


.. code-block:: python

    import pickle

    with open('app_data.pickle', 'rb') as file:
        phone_book = pickle.load(file)


Wykonanie dowolnego kodu
------------------------

**Za pomocą modułu pickle należy deserializować dane pochodzące wyłącznie z zaufanego źródła.**

Powyższe stwierdzenie jest bardzo ważne. Dobrze obrazuje to przykład, który deserializuje ciąg bajtów podany przez złośliwego użytkownika (albo atakującego).


.. code-block:: python

    import pickle

    bytes = b"cos\nsystem\n(S'echo Usuwanie plikow.'\ntR."

    pickle.loads(bytes)


W strumieniu danych znajduje się wywołanie funkcji ``system()``, która uruchamia podane polecenie w konsoli.


Literatura
----------

1. `pickle — Python object serialization <https://docs.python.org/3/library/pickle.html>`__
2. `Don't Pickle Your Data <https://www.benfrederickson.com/dont-pickle-your-data/>`__
