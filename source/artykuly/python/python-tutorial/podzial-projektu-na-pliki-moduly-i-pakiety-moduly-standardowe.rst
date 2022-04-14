Podział projektu na pliki - Moduły i pakiety, moduły standardowe
================================================================

.. pdfobject:: /_static/files/artykuly/python/python-tutorial/Podzial-projektu-na-pliki-Moduly-i-pakiety-moduly-standardowe.pdf


Moduły
------

**Modułem** nazywamy plik tekstowy zawierający kod źródłowy napisany w języku Python. Mogą znajdować się w nim elementy takie jak definicje funkcji, klas, zmiennych.

**Nazwa modułu** to nazwa pliku bez rozszerzenia.

Nazwy (np. funkcje, klasy, zmienne) znajdujące się w modułach mogą być importowane do modułu nad którym pracujemy. Zaimportować, czyli sprawić, aby dana nazwa stała się dostępna.

**Sposoby importowania modułów i nazw**:

1. **zaimportowanie całego modułu**

.. code:: python

    import MODUŁ

Przykład:

    *Plik utils.py*

    .. code:: python

        def czy_liczba(napis):
            # ...
            return True

    *Plik kalkulator.py*

    .. code:: python

        import utils

        print("czy_liczba():", utils.czy_liczba("13"))


2. **zaimportowanie całego modułu pod nową nazwą**

.. code:: python

    import MODUŁ as NOWA_NAZWA

Przykład:

    *Plik utils.py*

    .. code:: python

        def czy_liczba(napis):
            # ...
            return True

    *Plik kalkulator.py*

    .. code:: python

        import utils as narzedzia

        print("czy_liczba():", narzedzia.czy_liczba("13"))


3. **zaimportowanie wybranych nazw**

.. code:: python

    from MODUŁ import NAZWA1, NAZWA2
    
Przykład:

    *Plik utils.py*

    .. code:: python

        def czy_liczba(napis):
            # ...
            return True

    *Plik kalkulator.py*

    .. code:: python

        from utils import czy_liczba

        print("czy_liczba():", czy_liczba("13"))


4. **zaimportowanie wybranej nazwy pod nową nazwą**

.. code:: python

   from MODUŁ import NAZWA as NOWA_NAZWA

Przykład:

    *Plik utils.py*

    .. code:: python

        def czy_liczba(napis):
            # ...
            return True

    *Plik kalkulator.py*

    .. code:: python

        from utils import czy_liczba as sprawdz
        from math import ceil as sufit, floor as podloga

        print("czy_liczba():", sprawdz("13"))
        print("sufit():", sufit(3.3))
        print("podloga():", podloga(3.3))


5. **zaimportowanie wszystkich nazw z danego modułu**

.. code:: python

   from MODUŁ import *

Przykład:

    *Plik utils.py*

    .. code:: python

        def czy_liczba(napis):
            # ...
            return True

    *Plik kalkulator.py*

    .. code:: python

        from utils import *

        print("czy_liczba():", czy_liczba("13"))


Podczas importowania nazw trzeba uważać. Która z poniższych funkcji ``czy_liczba`` zostanie wywołana?

*Plik utils.py*

.. code:: python

    def czy_liczba(napis):
        # ...
        return True

*Plik kalkulator.py*
    
.. code:: python

    from utils import *

    def czy_liczba(x):
        # ...
        return False

    print("czy_liczba():", czy_liczba("13"))


**Podczas importowania modułu jego kod źródłowy jest interpretowany i wykonywany.** Może to powodować niepożądane zachowanie.

Specjalna zmienna ``__name__`` przechowuje nazwę modułu w postaci napisu. Wartość ``__main__`` oznacza, że moduł ten został uruchomiony bezpośrednio przez użytkownika.

Sprawdzenie wartości zmiennej ``__name__`` w module pozwala uniknąć wykonywania kodu modułu podczas jego importowania.

Przykład:

    *Plik utils.py*

    .. code:: python

        def czy_liczba(napis):
            pass

        print("utils: Kod modułu.")
        print("utils: Wartość zmiennej __name__ to:",
              __name__)

    *Plik kalkulator.py*

    .. code:: python

        import utils

        print("kalkulator: Kod głównego programu.")
        print("kalkulator: Wartość zmiennej __name__ to:",
              __name__)


Uruchomienie modułu kalkulator spowoduje wykonanie kodu znajdującego się w module ``utils``. Na ekranie zostaną wyświetlone linie zaczynające się od ``utils:`` oraz ``kalkulator:``.

Rozwiązaniem jest sprawdzenie wartości zmiennej ``__name__`` w module ``utils``. Za pomocą instrukcji warunkowej należy zdecydować, czy określony fragment kodu ma zostać wykonany.

Przykład:

    *Plik utils.py*

    .. code:: python

        def czy_liczba(napis):
            pass

        if __name__ == "__main__":
            print("utils: Kod modułu.")
            print("utils: Wartość zmiennej __name__ to:",
                  __name__)

    *Plik kalkulator.py*

    .. code:: python

        import utils

        print("kalkulator: Kod głównego programu.")
        print("kalkulator: Wartość zmiennej __name__ to:",
              __name__)


Pakiety
-------

**Pakiety** są sposobem na uporządkowanie modułów, jest **to kolekcja modułów**.

Fizycznie pakiet jest katalogiem mogącym [#ImplicitNamespacePackages]_ zawierać:

* specjalny moduł o nazwie ``__init__`` - w najprostszym przypadku jest to pusty plik, może także zawierać kod inicjalizujący pakiet (np. ustawienie zmiennych),
* moduły,
* pakiety.


.. [#ImplicitNamespacePackages] dla wtajemniczonych: od Pythona 3.3 plik __init__.py jest opcjonalny, zachowanie to opisano w PEP 420 -- Implicit Namespace Packages, https://www.python.org/dev/peps/pep-0420/ 


Przykładowa struktura katalogów projektu:

.. code:: text

    .
    |-- kalkulator.py
    `-- utils
        |-- __init__.py      (opcjonalny)
        |-- strings.py
        `-- user.py

Moduł ``kalkulator`` jest głównym skryptem do uruchomienia przez użytkownika.

Pakiet ``utils`` jest wykorzystywany przez moduł kalkulator.

Sposoby importowania nazw **z pakietów**:

1. ``from PAKIET.MODUL import NAZWA``

Przykład:

    *Plik utils/strings.py*

    .. code:: python

        def czy_liczba(napis):
            # ...
            return True

    *Plik kalkulator.py*

    .. code:: python

        from utils.strings import czy_liczba

        print("czy_liczba():",
              czy_liczba("13"))


2. ``import PAKIET.MODUL``

Przykład:

    *Plik utils/strings.py*

    .. code:: python

        def czy_liczba(napis):
            # ...
            return True

    *Plik kalkulator.py*

    .. code:: python

        import utils.strings

        print("czy_liczba():",
              utils.strings.czy_liczba("13"))


3. ``import PAKIET`` (wymaga pliku __init__.py)

Przykład:

    *Plik utils/strings.py*

    .. code:: python

        def czy_liczba(napis):
            # ...
            return True

    *Plik utils/__init__.py*

    .. code:: python

        from . import strings

    *Plik kalkulator.py*

    .. code:: python

        import utils

        print("czy_liczba():",
              utils.strings.czy_liczba("13"))

Sposób importowania nazw **w obrębie pakietu**:

Przykład:

    *Plik utils/strings.py*

    .. code:: python

        def czy_liczba(napis):
            # ...
            return True

    *Plik utils/user.py*

    .. code:: python

        from .strings import czy_liczba

        def pobierz_liczbe():
            napis = input("Podaj liczbe:")
            if czy_liczba(napis):
               return int(napis)
            else:
               return False

Ten sposób importowania nazw może być również stosowany w pliku ``__init__.py``.


Moduły standardowe
------------------

Python jest dostarczany wraz z szeroką gamą modułów, ich pełną listę można znaleźć na stronie: https://docs.python.org/3/library/


Literatura
----------

1. `Moduły i pakiety <https://docs.python.org/3/tutorial/modules.html>`__
2. `Lista wbudowanych pakietów Pythona <https://docs.python.org/3/library/>`__
