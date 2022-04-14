Funkcje - Definicja i wywołanie funkcji, przekazywanie argumentów, zwracanie wartości
=====================================================================================

.. pdfobject:: /_static/files/artykuly/python/python-tutorial/Funkcje-Definicja-i-wywolanie-funkcji-przekazywanie-argumentow-zwracanie-wartosci.pdf


Funkcje w matematyce
--------------------

**Funkcja** *(łac. functio, -onis „odbywanie, wykonywanie, czynność”)* – dla danych dwóch zbiorów **X** i **Y**  przyporządkowanie każdemu elementowi zbioru **X** dokładnie jednego elementu zbioru **Y**. [#funkcja_wikipedia]_

Przykład::

  f(x) = x + 1

  y = f(4)
  y = 4 + 1
  y = 5


.. [#funkcja_wikipedia] https://pl.wikipedia.org/wiki/Funkcja


Definicja i wywołanie funkcji
-----------------------------

Funkcja to wydzielona część programu wykonująca pewne operacje. Nazwa funkcji ma istotne znaczenie, określa ona czynność, którą dana funkcja wykonuje. Poprzez użycie odpowiedniej nazwy można wywołać konkretną funkcję, czyli wykonać kod w niej zapisany.

Dobrze napisana funkcja wykonuje tylko jedną czynność. 

Tworzenie funkcji w języku Python rozpoczynamy od słowa kluczowego def. Zaraz po nim następuje nazwa funkcji, nawiasy okrągłe oraz dwukropek.
Przypomnijmy: dwukropek na końcu linii oznacza, że w kolejnej linii następuje odpowiednio wcięty blok kodu złożony z co najmniej jednej linii.

.. code-block:: python

    def czesc():
        print("Czesc!")

    czesc()

Każdy blok kodu powinien zawierać dokładnie cztery spacje. Jest to wymaganie określone w dokumencie PEP 8, do którego zaleceń stosują się programiści Pythona.


Przekazywanie argumentów
------------------------

Parametry funkcji umieszczane są w nawiasach okrągłych umieszczonych za nazwą funkcji. Argumenty przekazujemy w nawiasach okrągłych podczas wywoływania funkcji.


.. code-block:: python

    def czesc(imie):
        print("Czesc " + imie + "!")

    czesc("Janusz")

Podczas przekazywania argumentu możemy również podać nazwę parametru.

.. code-block:: python

    def czesc(imie):
        print("Czesc " + imie + "!")

    czesc(imie="Janusz")


**Pytanie**

Załóżmy, że mamy funkcję przyjmującą dwa parametry: ``imie`` oraz ``miasto``.

Czy korzystając z nazw parametrów możemy zmienić kolejność ich występowania?

.. code-block:: python

    def czesc(imie, miasto):
        print("Czesc " + imie + "!")
        print("Widze, ze jestes z miasta", miasto)

    czesc(miasto="Wroclaw", imie="Janusz")

Odpowiedź: Tak.


**Pytanie**

Załóżmy, że mamy funkcję przyjmującą dwa parametry:: ``imie`` oraz ``miasto``.

Czy program zadziała dobrze, gdy przekażemy argumenty ze zmienioną kolejnością nie podając nazw parametrów?

.. code-block:: python

    def czesc(imie, miasto):
        print("Czesc " + imie + "!")
        print("Widze, ze jestes z miasta", miasto)

    czesc("Wroclaw", "Janusz")

Odpowiedź: Nie.


Przekazywanie argumentów - Argumenty domyślne
---------------------------------------------

Dla parametry funkcji można ustanowić pewne konkretne wartości, nazywamy je **argumentami domyślnymi**.

Argumenty domyślne pozwalają wywołać funkcję bez podawania jednego lub większej liczby argumentów.

.. code-block:: python

    def czesc(imie, miasto, komunikat="Czesc"):
        print(komunikat, imie + "!")
        print("Widze, ze jestes z miasta", miasto)

    czesc("Janusz", "Wroclaw")
    czesc("Alicja", "Wroclaw", "Milego dnia")


**Pytanie**

Czy argument domyślny możemy przypisać do parametru miasto?

Innymi słowy, czy dowolny parametr bez podanego argumentu domyślnego może znajdować się za parametrami z argumentami domyślnymi?

.. code-block:: python

    def czesc(imie, miasto="Wroclaw", komunikat):
        print(komunikat, imie + "!")
        print("Widze, ze jestes z miasta", miasto)

    czesc("Alicja", "Milego dnia")

Odpowiedź: Nie.


Zwracanie wartości
------------------

Z czasem stopień skomplikowania naszych funkcji rośnie, ich zadaniem będzie wykonanie pewnych obliczeń i zwrócenie wyniku.

Wartości z funkcji zwracane są przy pomocy słowa kluczowego return.

.. code-block:: python 

    def dodawanie(a, b):
        z = a + b
        return z

    wynik = dodawanie(2, 3)
    print("Wynik:", wynik)


**Pytanie**

Co to znaczy zwrócić wartość z funkcji?

Odpowiedź: Bardzo ogólnie możemy powiedzieć, że zwrócenie wartości oznacza podstawienie obliczonego wyniku (wartości wskazanej słowem return) w miejsce wywołania funkcji.


Wartości zwracane z funkcji nie muszą być tylko liczbami. Funkcje mogą zwracać dowolne obiekty (np. listy, krotki, słowniki).

**Pytanie**

Co robi poniższy kod?

.. code-block:: python

    def produce_numbers(n):
        i = 0
        numbers = []
        while i < n:
            numbers.append(i)
            i = i + 1
        return numbers

    for i in produce_numbers(5):
        print("Element:", i)


Przekazywanie argumentów - ciąg dalszy
--------------------------------------

Funkcje w języku Python mogą przyjmować dowolnie wiele argumentów. W tym celu został opracowany specjalny parametr ``*args`` przechowujący dodatkowe nienazwane argumenty przekazane do funkcji.

Nazwa  ``args`` jest umowna.

.. code-block:: python

    def czesc(imie, *args):
        print("Czesc " + imie + "!")
        for s in args:
            print("Czesc " + s + "! (args)")

    czesc("Janusz", "Maciej", "Mateusz")


Dostępny jest także parametr ``**kwargs`` przechowujący dodatkowe nazwane argumenty przekazane do funkcji.  ``kwargs`` jest słownikiem, gdzie kluczem jest nazwa parametru, a wartością przekazany argument.

Nazwa ``kwargs`` jest umowna.

.. code-block:: python

    def czesc(imie, **kwargs):
        nazwa = imie
        if "nazwisko" in kwargs:
            nazwa = nazwa + " " + kwargs["nazwisko"]
        print("Czesc " + nazwa + "!")

    czesc("Janusz")
    czesc("Anna", nazwisko='Nowak')


Literatura
----------

1. `Funkcje <https://docs.python.org/3/tutorial/controlflow.html#defining-functions>`__
2. `Więcej o funkcjach <https://docs.python.org/3/tutorial/controlflow.html#more-on-defining-functions>`__
