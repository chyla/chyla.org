xrange() nie jest generatorem
=============================


Spis treści
-----------

1. Wstęp
2. Koncepcja generatora
3. xrange a generator
4. Wnioski


Wstęp
-----

W Pythonie 2 dostępne są funkcje ``range()`` oraz ``xrange()``. Wartością zwracaną przez ``range()`` jest lista kolejnych liczb całkowitych, ``xrange()`` zwraca obiekt pozwalający na wytworzenie kolejnych liczb tylko wtedy, gdy jest to potrzebne. W Pythonie 3 funkcja ``range()`` została usunięta, zastąpiła ją ``xrange()`` pod nową nazwą ``range()``:

.. code-block::

    $ python2
    Python 2.7.13 (default, Nov 24 2017, 17:33:09) 
    [GCC 6.3.0 20170516] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> range(1,5)
    [1, 2, 3, 4]
    >>> xrange(1,5)
    xrange(1, 5)


.. code-block::

    $ python3
    Python 3.5.3 (default, Jan 19 2017, 14:11:04) 
    [GCC 6.3.0 20170118] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> range(1,5) # dawniej xrange()
    range(1, 5)

W dalszej części mowa jest o funkcji `range()` w kontekście Pythona 3.


Koncepcja generatora
--------------------

Dość szczegółowo generatory `opisałem już na swoim blogu [2] </artykuly/python/python-dekoratory.html>`__. We wspomnianym wpisie podałem następujący opis generatora:

    Generator jest pewnego rodzaju funkcją. Funkcja ta może zostać wstrzymana oraz wznowiona od miejsca, w którym została wstrzymana. Na podstawie zapamiętanego stanu możliwe jest zwracanie różnych wartości podczas kolejnych wstrzymań funkcji. [..] Taką funkcję nazywamy funkcją generującą (ang. generator function). Jej wywołanie spowoduje utworzenie generatora - obiektu generującego (ang. generator object, generator-iterator).

    Generatory cechuje leniwa ewaluacja (ang. lazy evaluation), czyli tworzenie kolejnych elementów dopiero przy odwołaniu się do generatora. Technika ta pozwala zredukować liczbę wykonywanych obliczeń, zmniejszyć wykorzystanie pamięci oraz tworzyć nieskończoną ilość elementów.

Generator jako obiekt posiada także określony interfejs, w jego skład wchodzą funkcje ``send()``, ``throw()`` oraz ``close()``, a także ``__next__()`` w przypadku Pythona 3 i ``next()`` w Pythonie 2:

.. code-block::

    $ python3
    Python 3.5.3 (default, Jan 19 2017, 14:11:04) 
    [GCC 6.3.0 20170118] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> g = (x for x in range(5))
    >>> type(g)
    <class 'generator'>
    >>> dir(g)
    ['__class__', '__del__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__iter__', '__le__', '__lt__', '__name__', '__ne__', '__new__', '__next__', '__qualname__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'close', 'gi_code', 'gi_frame', 'gi_running', 'gi_yieldfrom', 'send', 'throw']


xrange a generator
------------------

``range()`` jest podobny w działaniu do generatora – tworzy kolejne elementy na żądanie. Funkcja ``range()`` nie tworzy jednak obiektu generującego, tworzona jest natomiast instancja klasy ``range``:

.. code-block::

    Python 3.5.3 (default, Jan 19 2017, 14:11:04) 
    [GCC 6.3.0 20170118] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> x = range(1, 5)
    >>> type(x)
    <class 'range'>


W Pythonie 2 nie jest to instancja klasy ``range``, a obiekt typu ``xrange``:

.. code-block::

    $ python2
    Python 2.7.13 (default, Nov 24 2017, 17:33:09) 
    [GCC 6.3.0 20170516] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> x = xrange(1, 5)
    >>> type(x)
    <type 'xrange'>


Klasa ``range`` nie implementuje także interfejsu generatora:

.. code-block::

    $ python3
    Python 3.5.3 (default, Jan 19 2017, 14:11:04) 
    [GCC 6.3.0 20170118] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> x = range(1, 5)
    >>> dir(x)
    ['__class__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'count', 'index', 'start', 'step', 'stop']


Jak zaprezentowano na powyższym wydruku, obiekt klasy range nie zawiera żadnej z metod ``send()``, ``throw()``, ``close()`` czy ``__next__()``. Wykorzystywany jest natomiast protokół iteratorów — wskazuje na to obecność funkcji ``__iter__()``. ``range`` jest obiektem iterowalnym.


Wnioski
-------

``range()`` nie jest generatorem, swoje działanie opiera na protokole iteratorów. Wyszukanie frazy ‘`xrange generator <https://www.google.pl/search?q=xrange+generator>`__’[3] w wyszukiwarce Google zwraca całkiem sporo wyników, w których to autorzy poszczególnych tekstów określają ``xrange()`` jako generator, co — jak już wykazałem — nie jest poprawne.


Literatura
----------

1. `PEP 260 -- Simplify xrange() <https://www.python.org/dev/peps/pep-0260/>`__
2. `Python - Generatory </artykuly/python/python-dekoratory.html>`__
3. `Google: xrange generator <https://www.google.pl/search?q=xrange+generator>`__

