Python - Generatory
===================

Spis treści
-----------

1. Wstęp

2. Generator prosty
  
   - funkcja generująca
   - funkcja generująca a generator

3. Wyrażenie generujące
  
4. Generator rozszerzony

   - wysłanie wartości do generatora
   - metoda throw() oraz close()
   - podgenerator


.. note::

	Wszystkie przykłady pisane są z myślą o Pythonie w wersji 3.6.


Wstęp
-----

Bardzo ogólnie i jeszcze niezbyt precyzyjnie możemy powiedzieć, że generator jest pewnego rodzaju funkcją. Funkcja ta może zostać wstrzymana oraz wznowiona od miejsca, w którym została wstrzymana. Na podstawie zapamiętanego, stanu możliwe jest zwracanie różnych wartości podczas kolejnych wstrzymań funkcji.

Generatory cechuje `leniwa ewaluacja <https://pl.wikipedia.org/wiki/Warto%C5%9Bciowanie_leniwe>`__ (ang. `lazy evaluation <https://en.wikipedia.org/wiki/Lazy_evaluation>`__), czyli tworzenie kolejnych elementów dopiero przy odwołaniu się do generatora. Technika ta pozwala zredukować liczbę wykonywanych obliczeń, zmniejszyć wykorzystanie pamięci oraz tworzyć nieskończoną ilość elementów. 

Steven McConnell w swojej książce `Code Complete: A Practical Handbook of Software Construction <https://en.wikipedia.org/wiki/Code_Complete>`__ zauważa, iż wielkość projektu (mierzona według linii kodu) wpływa na liczbę popełnionych błędów. W podrozdziale *How Program Size Affects Construction* zawarta została informacja, że w projekcie o wielkości co najmniej 512 tys. linii kodu przypada od **4** do **100** błędów na każde **1 000** linii kodu (`defect density <http://softwaretestingfundamentals.com/defect-density/>`__). Im mniej kodu zawiera projekt, tym mniej błędów, prawdopodobnie, popełniono. W projektach mniejszych niż 2 000 linii kodu przypada od **0** do **50** błędów na **1 000** linii kodu.

W jaki sposób wiąże się to z omawianymi generatorami? Bardzo prosto - w Pythonie generatory tworzymy z wykorzystaniem specjalnego słowa kluczowego, na tej podstawie interpreter zapisuje stan funkcji oraz zwraca jej wynik. W językach, które nie wspierają generatorów, programista sam musi zadbać o zachowanie i przywrócenie stanu (np. implementując generator jako klasę), co ostatecznie wpływa na możliwość popełnienia błędu.


Generator prosty
----------------

Wiemy już jak działa generator, zobaczmy zatem na przykładzie, w jaki sposób utworzyć go w Pythonie. Poniżej zaprezentowany został generator zwracający kolejne liczby parzyste od 0 do 20:

.. code-block:: python

  def liczby():
      for i in range(11):
          yield i * 2
  
  for parzysta in liczby():
      print(parzysta)


Wynik działania skryptu::

    0
    2
    4
    6
    8
    10
    12
    14
    16
    18
    20

W pierwszych trzech liniach znajduje się generator. Elementem, po którym możemy odróżnić go od zwykłej funkcji jest słowo kluczowe `yield`. Odpowiada ono za przerwanie wykonania funkcji, zapisanie jej stanu  oraz zwrócenie wartości - w przykładzie `i * 2`.

Wznowiona funkcja rozpoczyna swoje działanie dokładnie w miejscu, w którym została wstrzymana. Zobaczmy to na kolejnym przykładzie:

.. code-block:: python

  def wznowienia():
      print("wstrzymuje dzialanie")
      yield 1
      print("wznawiam dzialanie")
  
      print("wstrzymuje dzialanie")
      yield 2
      print("wznawiam dzialanie")
  
  for i in wznowienia():
      print("Zwrocono wartosc: " + str(i))


Wynik działania skryptu::

    wstrzymuje dzialanie
    Zwrocono wartosc: 1
    wznawiam dzialanie
    wstrzymuje dzialanie
    Zwrocono wartosc: 2
    wznawiam dzialanie

W generatorze `wznowienia` (linie 1 - 8) widzimy dwie instrukcje `yield` zwracające odpowiednio `1` i `2`. Znajdują się w nim również instrukcje drukujące dodatkowe komunikaty z informacją o miejscu, które jest wykonywane. W pętli `for` (linia 10) wykorzystujemy generator.

Prześledźmy proces wykonania powyższego skryptu. Pętla (linia 10) aktywuje generator, wykonywana jest linia 2 oraz 3 - na ekranie zobaczyliśmy informację o wstrzymaniu działania generatora, wykonana została instrukcja `yield`, co wstrzymało generator, zapisało jego stan oraz zwróciło wartość `1`. Kolejnym krokiem było wykonanie ciała pętli `for`, czyli wydrukowanie na ekranie wartości zwróconej. Tak wyglądał pierwszy przebieg pętli.

W drugim przebiegu generator został wznowiony (linia 10), co spowodowało przywrócenie stanu generatora oraz kontynuację jego pracy od linii 4. Wykonane zostały dwie instrukcje drukujące dodatkowe informacje oraz kolejna instrukcja `yield` - ponownie generator został wstrzymany oraz zwrócona została wartość `2`, co potwierdza informacja wydrukowana z ciała pętli.

W trzecim przebiegu pętli (linia 10) generator został wznowiony od linii 8. Wykonano instrukcję drukującą napis na ekranie, ale tym razem generator nie zwrócił żadnej wartości, dlatego pętla została przerwana i jej ciało nie zostało wykonane.

Działanie generatora może również zostać przerwane poprzez wykonanie instrukcji return, co obrazuje poniższy przykład:

.. code-block:: python

  def ret():
      for i in range(5):
          if i == 3:
              return
          else:
              yield i
  
  for x in ret():
      print(x)


Wynik działania skryptu::

    0
    1
    2


Funkcja generująca a generator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

W powyższym rozumowaniu pozwoliłem sobie na dość ogólne podejście do pojęcia generator. O generatorze mówiłem, jako o funkcji zawierającej instrukcję `yield` - to jednak nie do końca jest prawdą. Funkcja zawierająca instrukcję `yield`, widoczna na powyższych przykładach, jest jedynie instrukcją, w jaki sposób interpreter ma utworzyć generator. Taką funkcję nazywamy **funkcją generującą** (ang. generator function).
**Jej wywołanie spowoduje utworzenie generatora** - obiektu generującego (ang. generator object, generator-iterator).

Zobaczmy to na przykładzie funkcji generującej nieskończoną ilość liczb parzystych:

.. code-block:: python

  def parzyste():
      i = 0
      while True:
          yield i
          i = i + 2


Funkcja ta jest **funkcją generującą**, jej wywołanie spowoduje **utworzenie generatora**::

    Python 3.6.3rc1 (default, Sep 20 2017, 10:53:18) 
    [GCC 7.2.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> def parzyste():
    ...     i = 0
    ...     while True:
    ...         yield i
    ...         i = i + 2
    ... 
    >>> gen = parzyste()
    >>> type(gen)
    <class 'generator'>
    >>> print(str(gen))
    <generator object parzyste at 0x7feb4ac0e0a0>

Na powyższym wydruku widać, że wywołanie funkcji generującej spowodowało zwrócenie obiektu generatora, a nie jakby się mogło wydawać liczby `2`. Dopiero operacje na obiekcie generatora pozwolą uzyskać kolejne liczby parzyste. **Obiekt generatora, generator przechowuje stan oraz zawiera odpowiednią metodę zwracającą kolejne wartości**::

    >>> gen.__next__()
    0
    >>> gen.__next__()
    2
    >>> gen.__next__()
    4
    >>> gen.__next__()
    6
    >>> next(gen)
    8

Powyższy wydruk przedstawia wywołanie metody `__next__()` oraz funkcji wbudowanej `next() <https://docs.python.org/2/library/functions.html#next>`__ zwracającej kolejno generowane wartości.

Mamy do czynienia z podwójnym znaczeniem słowa generator - jedno to określenie funkcji generującej, a drugie to określenie obiektu generującego (właściwego generatora), o czym wspomina sama dokumentacja (PEP 255):

    Note that when the intent is clear from context, the unqualified name "generator" may be used to refer either to a generator-function or a generator-iterator.


Wyrażenie generujące
--------------------

Użycie funkcji generującej nie jest jedynym sposobem na utworzenie generatora. Bardzo często wykorzystywane są także wyrażenia generujące (ang. generator expression), w użyciu bardzo podobne do `wyrażeń listowych <https://pl.wikibooks.org/wiki/Zanurkuj_w_Pythonie/Odwzorowywanie_listy>`__ (ang. `list comprehension <https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions>`__).

Zobaczmy przykład tworzący listę złożoną z 6 elementów::

    Python 3.6.3rc1 (default, Sep 20 2017, 10:53:18) 
    [GCC 7.2.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> elements = [x * 2 for x in range(6)]
    >>> elements
    [0, 2, 4, 6, 8, 10]

Każdy z elementów listy musiał zostać utworzony podczas jej tworzenia, dodatkowo zajmuje miejsce w pamięci. W przypadku wyrażeń generujących, obiekt tworzony jest tylko w momencie zapytania. Poniżej przykład wyrażenia generującego::

    Python 3.6.3rc1 (default, Sep 20 2017, 10:53:18) 
    [GCC 7.2.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> elements = (x * 2 for x in range(6))
    >>> elements
    <generator object <genexpr> at 0x7fcbb0304bf8>
    >>> next(elements)
    0
    >>> next(elements)
    2
    >>> next(elements)
    4

Nawiasy mogą zostać pominięte w przypadku wywołań z jednym argumentem, np. podczas wywołania funkcji::

    Python 3.6.3rc1 (default, Sep 20 2017, 10:53:18) 
    [GCC 7.2.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> def f(x):
    ...     print(str(type(x)))
    ... 
    >>> f(x for x in range(6))
    <class 'generator'>


Generator rozszerzony
---------------------

W Pythonie 2.5 interfejs generatorów rozszerzono między innymi o możliwość przekazania wartości w miejsce, w którym nastąpiło wstrzymanie (zachęcam zapoznać się z dokumentem PEP 342 w celu poznania szczegółów). Wykorzystano do tego wyrażanie `yield`, którego wartość może zostać przypisana do zmiennej. W celu przekazania nowej wartości do generatora należy wywołać na nim funkcję `send()`.

Poniżej przykład generatora dodającego liczbę 1:

.. code-block:: python

  def gen():
      x = 0   
      while True:
          y = yield x
          if y is None:
              x = x + 1
          else:
              x = y
  
  g = gen()
  
  print(next(g))
  print(next(g))
  print(next(g))
  
  print(g.send(12))
  print(next(g))
  print(next(g))


W porównaniu do poprzednich przykładów, główna zmiana widoczna jest w linii 4. Wynik wyrażenia `yield` zostaje przypisany do nazwy `y`. Wywołanie generatora funkcją `next()` spowoduje zwrócenie wartości `None`, natomiast wywołanie funkcją `send()` spowoduje zwrócenie wartości przekazanej.

Wynik działania powyższego skryptu powinien zobrazować działanie generatora::

    0
    1
    2
    12
    13
    14

Generatory zostały także wzbogacone o metody `throw()` oraz `close()`. `throw()` powoduje rzucenie wyjątku w miejscu, w którym generator został wstrzymany oraz ewentualne zwrócenie kolejnej wygenerowanej wartości. `close()` kończy pracę generatora poprzez rzucenie wyjątku `GeneratorExit` za pomocą funkcji `throw()`.

Szczegóły działania metod `send()`, `throw()` oraz `close()` bardzo przejrzyście zostały przedstawione w dokumencie `PEP 342 <https://www.python.org/dev/peps/pep-0342/#specification-summary>`__:

    2. Add a new send() method for generator-iterators, which resumes the generator and sends a value that becomes the result of the current yield-expression. The send() method returns the next value yielded by the generator, or raises StopIteration if the generator exits without yielding another value.
    
    3. Add a new throw() method for generator-iterators, which raises an exception at the point where the generator was paused, and which returns the next value yielded by the generator, raising StopIteration if the generator exits without yielding another value. (If the generator does not catch the passed-in exception, or raises a different exception, then that exception propagates to the caller.)
    
    4. Add a close() method for generator-iterators, which raises GeneratorExit at the point where the generator was paused. If the generator then raises StopIteration (by exiting normally, or due to already being closed) or GeneratorExit (by not catching the exception), close() returns to its caller. If the generator yields a value, a RuntimeError is raised. If the generator raises any other exception, it is propagated to the caller. close() does nothing if the generator has already exited due to an exception or normal exit.

Poniżej przykład prezentujący działanie metody `throw()` oraz `close()`::

    Python 3.6.3rc1 (default, Sep 20 2017, 10:53:18) 
    [GCC 7.2.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> def gen():
    ...     while True:
    ...         try:
    ...             yield 1
    ...         except GeneratorExit:
    ...             print("wyjatek zostal rzucony!")
    ...             return
    ... 
    >>> g = gen()
    >>> next(g)
    1
    >>> g.throw(GeneratorExit)
    wyjatek zostal rzucony!
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    StopIteration
    >>> 
    >>> g2 = gen()
    >>> next(g2)
    1
    >>> g2.close()
    wyjatek zostal rzucony!
    

Podgenerator
^^^^^^^^^^^^

Z funkcji wieloliniowej można w prosty sposób wydzielić mniejsze funkcje, dokonać refaktoryzacji kodu i oddelegować zadania do mniejszych funkcji. Czy możemy w ten sam sposób postąpić z generatorami i zadania jednego generatora oddelegować do innego?

Okazuje się, że nie jest to takie proste. Jednym z pomysłów jest utworzenie generatora w generatorze i odpytywanie go o kolejne wartości, jak pokazano to na poniższym przykładzie:

.. code-block:: python

  def gen012():
      for i in range(3):
          yield i
  
  def gen01234():
      g = gen012()
  
      for i in range(3):
          yield next(g)
  
      yield 3
      yield 4
  
  for i in gen01234():
      print(i)


Wynik działania skryptu::

    0
    1
    2
    3
    4

Jest to pewne rozwiązanie, jednak co w sytuacji, gdy na generatorze `gen01234` będziemy chcieli wywołać jedną z metod przedstawionych wcześniej, np. `throw()`? Z którego miejsca zostanie rzucony wyjątek, a z którego powinien zostać rzucony? Zobaczmy przykład:

.. code-block:: python

  class MojWyjatek(BaseException):
      pass
  
  def gen012():
      try:
          for i in range(3):
              yield i
      except MojWyjatek:
          print("wyjatek zostal rzucony w gen012!")
          raise # przekazujemy wyjątek dalej
  
  def gen01234():
      try:
          for i in gen012():
              yield i
  
          yield 3
          yield 4
      except MojWyjatek:
          print("wyjatek zostal rzucony w gen01234!")
  
  
  g = gen01234()
  next(g)
  g.throw(MojWyjatek)


Wynik działania skryptu::

    wyjatek zostal rzucony w gen01234!
    Traceback (most recent call last):
    File "/tmp/a.py", line 24, in <module>
        g.throw(MojWyjatek)
    StopIteration

Moglibyśmy spodziewać się, że wyjątek zostanie rzucony z `gen012()`, a tak się nie stało. By w pełni oddelegować zadania do innego generatora - podgeneratora (ang. subgenerator), w Pythonie 3.3 (PEP 380) wprowadzono konstrukcję `yield from`. Zobaczmy przykład pierwszy, zmodyfikowany o nową konstrukcję:

.. code-block:: python

  def gen012():
      for i in range(3):
          yield i
  
  def gen01234():
      yield from gen012()
      yield 3
      yield 4
  
  for i in gen01234():
      print(i)


Wynik działania skryptu::

    0
    1
    2
    3
    4

Widzimy, że kod generatora `gen01234()` jest któtszy i bardziej przejrzysty. Sprawdźmy zatem, z którego miejsca zostanie rzucony wyjątek z funkcji `throw()`:

.. code-block:: python

  class MojWyjatek(BaseException):
      pass
  
  def gen012():
      try:
          for i in range(3):
              yield i
      except MojWyjatek:
          print("wyjatek zostal rzucony w gen012!")
          raise # przekazujemy wyjątek dalej
  
  def gen01234():
      try:
          yield from gen012()
          yield 3
          yield 4
      except MojWyjatek:
          print("wyjatek zostal rzucony w gen01234!")
  
  
  g = gen01234()
  next(g)
  g.throw(MojWyjatek)


Wynik działania skryptu::

    wyjatek zostal rzucony w gen012!
    wyjatek zostal rzucony w gen01234!
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    StopIteration

Przykład ten pokazuje, że w pełni oddelegowaliśmy pracę do podgeneratora.


Literatura
----------

1. `Introduction to Python Generators <http://intermediatepythonista.com/python-generators>`__
2. `PEP 255 -- Simple Generators <https://www.python.org/dev/peps/pep-0255/>`__
3. `Co nowego w Pythonie 2.3 - PEP 255: Proste generatory <https://pl.python.org/docs/whatsnew/section-generators.html>`__
4. `PEP 289 -- Generator Expressions <https://www.python.org/dev/peps/pep-0289/>`__
5. `The Python Language Reference » 6. Expressions <https://docs.python.org/3.6/reference/expressions.html#generator-expressions>`__
6. `PEP 342 -- Coroutines via Enhanced Generators <https://www.python.org/dev/peps/pep-0342/>`__
7. `PEP 380 -- Syntax for Delegating to a Subgenerator <https://www.python.org/dev/peps/pep-0380/>`__
8. `Python generator cheatsheet <https://www.pythonsheets.com/notes/python-generator.html>`__
9. `Iterators, generators and decorators <http://pymbook.readthedocs.io/en/latest/igd.html>`__
