(Write-Up) Misja 003 - Długie obliczenia
========================================

Write-up z misji Gynvaela Coldwinda, treść misji została zaprezentowana na końcu streamu `Gynvael's Livestream #39: RPC, czyli zdalne API <https://www.youtube.com/watch?v=xR0hAJPp1vs>`__. Dla przypomnienia umieszczam ją, wraz z dodatkowym kodem źródłowym, poniżej::

  MISJA 003            goo.gl/ZPQvV0               DIFFICULTY: ██░░░░░░░░ [2/10]

  Tym razem nie trzeba nic robić. Wystarczy uruchomić poniższy skrypt, chwilkę
  poczekać, a hasło zostanie wypisane. No, taką dłuższą chwilkę...

.. code:: python

  #!/usr/bin/python
  def magic1(a, b):
    o = 0
    i = 0
    while i < a:
      o += 1
      i += 1
    i = 0
    while i < b:
      o += 1
      i += 1
    return o
  def magic2(a, b):
    o = 0
    i = 0
    while i < b:
      o = magic1(o, a)
      i += 1
    return o
  n1 = int("2867279575674690971609643216365"
           "4161626212087501848651843132337"
           "3373323997065608342")
  n2 = int("1240905467219837578349182398365"
           "3459812983123659128386518235966"
           "4109783723654812937")
  n = magic2(magic1(n1, n2), 1337)
  print hex(n)[2:-1].decode("hex").splitlines()[0]


W kodzie źródłowym widzimy dwie funkcje - ``magic1`` i ``magic2``.

Spójrzmy na pierwszą z nich. Jest to funkcja realizująca operację dodawania dwóch liczb, wykonana za pomocą dwóch pętli ``while``, by spowolnić obliczenia.

Druga funkcja realizuje operację mnożenia. Podobnie jak poprzednia, również została wykonana za pomocą pętli ``while``, by spowolnić obliczenia.

Zmieńmy, więc implementację tych dwóch funkcji i spróbujmy wykonać skrypt. Jest on napisany w Pythonie 2 - możemy to poznać po wywołaniu instrukcji ``print``:

.. code:: python

  #!/usr/bin/python
  
  def magic1(a, b):
      return a + b
  
  def magic2(a, b):
      return a * b
    
  n1 = int("2867279575674690971609643216365"
           "4161626212087501848651843132337"
           "3373323997065608342")
  n2 = int("1240905467219837578349182398365"
           "3459812983123659128386518235966"
           "4109783723654812937")
  n = magic2(magic1(n1, n2), 1337)
  print hex(n)[2:-1].decode("hex").splitlines()[0]


Wynik działania::

  Haslo: "WolneOprogramowanie!"

Mamy flagę, ale co dzieje się w drugiej części programu?


Big integers
------------

Python posiada wsparcie dla dużych liczb. W poniższym przykładzie mogą zdziwić tylko znaki cudzysłowia:

.. code:: python

  n1 = int("2867279575674690971609643216365"
           "4161626212087501848651843132337"
           "3373323997065608342")
  n2 = int("1240905467219837578349182398365"
           "3459812983123659128386518235966"
           "4109783723654812937")


Trzy napisy, widoczne w każdej z definicji zmiennej, zostaną złączone w jeden napis (zupełnie jak w języku C) i zamienione na typ ``int``. Spójrzmy na inny przykład::

  # python2
  >>> i = int("1" "0" "2" "4")
  >>> print i
  1024
  >>> i = i + 3
  >>> print i
  1027

W `dokumentacji Pythona 2 <https://docs.python.org/2.7/library/functions.html#int>`__ funkcja `int` została opisana następująco:

  Return an integer object constructed from a number or string x, or return 0 if no arguments are given. If x is a number, it can be a plain integer, a long integer, or a floating point number. If x is floating point, the conversion truncates towards zero. If the argument is outside the integer range, the function returns a long object instead.

Z opisu możemy wyczytać, że przyjmuje ona jako parametr obiekt typu ``string``. Ponadto nie musi zwrócić obiektu typu `int` — w przypadku przekroczenia jego zakresu, zostanie zwrócony obiekt typu ``long``.


Encode, Decode
--------------

Zwróćmy uwagę na dwie ostatnie linie kodu:

.. code:: python

  n = magic2(magic1(n1, n2), 1337)
  print hex(n)[2:-1].decode("hex").splitlines()[0]


W pierwszej wykorzystywane są funkcje ``magic1`` oraz ``magic2``, co jak już ustaliliśmy, realizuje odpowiednio dodawanie i mnożenie. Ostatecznie nazwa `n` będzie wskazywała na obiekt reprezentujący liczbę.

Przejdźmy do linii drugiej. Widzimy tam funkcję ``hex``, według `dokumentacji <https://docs.python.org/2/library/functions.html#hex>`__ zamienia ona liczbę na ciąg znaków, reprezentujący wskazaną liczbę w postaci zapisu szesnastkowego.

Wiedząc, że funkcja ``hex`` zwraca napis, wykonujemy na nim operację wybrania fragmentu za pomocą `sliceów <https://docs.python.org/2/tutorial/introduction.html#strings>`__. Liczby ujemne oznaczają, że wybieramy znaki licząc od końca. Zobaczmy to na trochę prostszym przykładzie::

  # python2
  >>> i = 1234
  >>> s = hex(i)
  >>> print s
  0x4d2
  >>> print s[2:-1]
  4d

Funkcja `decode <https://docs.python.org/2/library/codecs.html#codecs.decode>`__ służy do konwersji ciągu bajtów na napis odpowiedni dla użytkownika. Najczęstszym przypadkiem użycia funkcji ``decode`` (i ``encode``) jest konwersja ciągu bajtów zawierających napis zakodowany w UTF-8. Zobaczmy::

  # python2
  >>> a = 'ąęł'
  >>> print len(a)
  6
  >>> b = a.decode('utf-8')
  >>> print len(b)
  3
  >>> print a
  ąęł
  >>> print b
  ąęł

Pod nazwą ``a`` kryje się napis zakodowany za pomocą UTF-8. Jest to tablica 6 bajtów — na jeden znak przypadają 2 bajty. Funkcja ``len`` zwraca długość tej właśnie tablicy, a nie ilość znaków. W takim przypadku należy zdekodować ciąg bajtów na napis w UTF-8. Od tej chwili Python 2 będzie wiedział, że ma do czynienia z napisem w UTF-8 i funkcja ``len`` będzie zwracała poprawną wartość. Oczywiście wykorzystanie ``len`` jest tylko jedną z możliwości.

Funkcja ``encode`` dokonuje operacji odwrotnej. Zamienia ona napis, na zakodowany ciąg bajtów::

  # python2
  >>> a = u'ałóę'
  >>> print len(a)
  4
  >>> b = a.encode('utf-8')
  >>> print len(b)
  7

O historii UTF i jego obsłudze w Pythonie 2 można przeczytać w `dokumentacji <https://docs.python.org/2/howto/unicode.html>`__.

W kodzie Gynvaela mamy do czynienia z konwersją ciągu znaków zapisanych szesnastkowo na czytelny dla człowieka tekst. Działa to na takiej samej zasadzie, jak opisana powyżej, tylko zastosowany został `inny algorytm zamiany <https://docs.python.org/2/library/codecs.html#standard-encodings>`__.


Wiemy, jak działa kod i znamy rozwiązanie. Zapraszam do przeczytania także `write-up z poprzedniej misji </blog/Misja_002_-_Ukrywanie_danych_Base64/>`__.
