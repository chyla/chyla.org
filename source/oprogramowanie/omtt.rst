Output Match Testing Tool
=========================

OMTT pozwala sprawdzić poprawność działania programu/skryptu. Narzędzie uruchamia
testowany system z określonym wejściem i sprawdza czy wypisywane informacje
oraz kod wyjścia zgadzają się z założeniami określonymi w teście.

Instalacja
----------

Zalecam instalację za pomocą `Zero Install - zdecentralizowanego systemu instalacji
oprogramowania <https://0install.net/>`__. Zero Install pobierze OMTT w bezpieczny
sposób i zadba o regularne aktualizacje.

Kod źródłowy oraz pakiety binarne dostępne są na `stronie projektu w serwisie
GitHub <https://github.com/chyla/OutputMatchTestingTool>`__.

Windows
^^^^^^^

1. Zainstaluj Zero Install: https://get.0install.net/#windows

.. figure:: /images/oprogramowanie/zero-install-setup.png

   Przycisk instalacji Zero Install.

2. Otwórz konsolę systemową i za pomocą Zero Install dodaj OMTT:

   .. code-block:: shell

       0install add omtt https://apps.chyla.org/omtt.xml

3. OMTT zostało zainstalowane, uruchom ponownie konsolę.

Linux
^^^^^

1. Zainstaluj Zero Install: https://get.0install.net/#linux-ubuntu

2. Otwórz konsolę systemową i za pomocą Zero Install dodaj OMTT:

   .. code-block:: shell

       0install add omtt https://apps.chyla.org/omtt.xml

3. OMTT zostało zainstalowane.

   Możliwe, że musisz zmodyfikować zmienną systemową ```PATH``. Zero Install
   wyświetli odpowiedni komunikat. W takim przypadku do pliku ``~/.bashrc``
   dopisz na końcu:

   .. code-block:: shell

       export PATH=/home/${USER}/bin:$PATH

Struktura testu
---------------

Każdy test składa się z wejścia oraz bloków weryfikujących wyjście.

Wejście umieszcza się w bloku ``RUN WITH INPUT``, przykład:

.. code-block:: text

    RUN
    WITH INPUT
    Hello world!


**Pełne sprawdzenie** standardowego wyjścia określa się w bloku ``EXPECT OUTPUT``, przykład:

.. code-block:: text

    EXPECT OUTPUT
    Hello world!


**Częściowe sprawdzenie** standardowego wyjścia określa się w bloku ``EXPECT IN OUTPUT``, przykład:

.. code-block:: text

    EXPECT IN OUTPUT
    Hello
    EXPECT IN OUTPUT
    world!


**Sprawdzenie kodu wyjścia** określa się w bloku ``EXPECT EXIT CODE``, przykład:

.. code-block:: text

    EXPECT EXIT CODE 0


**Przykład kompletnego testu** dla programu ``cat``:

.. code-block:: text

    RUN
    WITH INPUT
    Hello world!
    EXPECT OUTPUT
    Hello world!
    EXPECT EXIT CODE 0

W jednym teście bloków sprawdzających może być wiele. Omówienie każdego bloku
wraz z przykładami znajduje się w pliku `README.md <https://github.com/chyla/OutputMatchTestingTool>`__

Uruchomienie testu
------------------

Przykład uruchomienia testu dla programu
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Przykład polecenia uruchamiającego test znajdujący się w pliku ``cat-will_print_input_and_exit_with_zero.omtt`` dla programu ``cat``:

.. code-block:: shell

    omtt --sut /bin/cat cat-will_print_input_and_exit_with_zero.omtt


Przykład uruchomienia testu dla skryptu wymagającego interpretera
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Przykład polecenia uruchamiającego test znajdujący się w pliku ``python-hello.omtt`` dla skryptu napisanego w języku Python:

.. code-block:: shell

    omtt --interpreter /usr/bin/python3 --sut hello.py python-hello.omtt

