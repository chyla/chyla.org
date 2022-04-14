Wprowadzenie do języka Python - Pierwszy program
================================================


.. pdfobject:: /_static/files/artykuly/python/python-tutorial/Wprowadzenie-do-jezyka-Python-Pierwszy-program.pdf


Python
------

Język powstał na początku lat dziewięćdziesiątych, jego twórcą jest Guido van Rossum (do roku 2018 dożywotni dyktator [#bdfl]_ [#OriginOfBDFL]_ [#TransferOfPower]_).

Python to wysokopoziomowy język, w którym programista może szybko napisać własną aplikację. Krótki czas potrzebny do wytworzenia oprogramowania czyni z niego idealne narzędzie do prototypowania. Na uwagę zasługuje również fakt, że został zaprojektowany jako język interpretowalny, a pisanie w nim skryptów jest względnie łatwe.


Python jest jednym z najpopularniejszych języków programowania. Ową tezę potwierdzają rankingi popularności, w których Python znajduje się na wysokiej pozycji.



.. [#bdfl] https://pl.wikipedia.org/wiki/Benevolent_Dictator_for_Life
.. [#OriginOfBDFL] https://www.artima.com/weblogs/viewpost.jsp?thread=235725 
.. [#TransferOfPower] https://mail.python.org/pipermail/python-committers/2018-July/005664.html 
 

Wybrane zastosowania Pythona
----------------------------

Web:

* `Django <https://www.djangoproject.com/>`__
* `Flask <https://flask.palletsprojects.com/en/1.1.x/>`__

Testowanie:

* `unittest — Unit testing framework <https://docs.python.org/3/library/unittest.html>`__
* `pytest: helps you write better programs <https://docs.pytest.org/en/stable/>`_
* `tox <https://tox.readthedocs.io/en/latest/>`__
* `Robot Framework <https://robotframework.org/>`__

Data science:

* `pandas - Python Data Analysis Library <https://pandas.pydata.org/>`__
* `Matplotlib <https://matplotlib.org/>`__
* `NumPy <https://numpy.org/>`__

Skryptowanie:

* `click_ <https://click.palletsprojects.com/>`__


Język a interpreter
-------------------

**język programowania**, inform. narzędzie do formułowania programów dla komputerów; jest językiem formalnym, którego składnia określa zasady zapisu programów (w sposób jednoznaczny i łatwy do analizy), a semantyka przypisuje programom ich interpretację (określa efekty działania programu zapisanego w języku programowania). [#jp]_ 

**interpreter** [ang.], interpretator, inform. program wykonujący program zapisany w pewnym języku programowania w ten sposób, że tekst programu jest czytany i natychmiast wykonywany (odwrotnie niż w przypadku kompilatora, tłumaczącego tekst programu na postać, którą można potem wielokrotnie wykonywać); [#interpreter]_

.. [#jp] źródło: https://encyklopedia.pwn.pl/haslo/jezyk-programowania;3917948.html
.. [#interpreter] źródło: https://encyklopedia.pwn.pl/haslo/interpreter;3915168.html


Python 2 a Python 3
-------------------

Aktualnie dostępna jest wersja 3 języka, Python 2 nie jest już rozwijany.

Początkowo koniec wsparcia (dostarczanie poprawek błędów związanych z bezpieczeństwem [#py2relsched]_) wyznaczono na 2015 rok, jednak pod naciskiem społeczności okres ten wydłużono o 5 lat, aż do 1 stycznia 2020 roku.

.. [#py2relsched] https://www.python.org/dev/peps/pep-0373/ 


Wymagane oprogramowanie
-----------------------

Do rozpoczęcia pracy z językiem Python wymagane są dwa elementy:

* zainstalowany interpreter języka Python - skupiamy się na języku Python 3, dlatego wymagany jest interpreter właśnie tej wersji (zalecany interpreter to CPython w wersji co najmniej 3.7);
* edytor tekstu lub zintegrowane środowisko programistyczne - zalecanym środowiskiem jest PyCharm w wersji Community z co najmniej 2018 roku.

Możliwe jest również korzystanie z interpretera oraz środowiska programistycznego dostępnego online https://repl.it/ (niektórych zadań nie da się zrealizować przy pomocy tego narzędzia).


Hello World!
------------

.. code:: python

    imie = input("Podaj swoje imię: ")

    print("Cześć", imie)


* brak funkcji głównej (np. main)
* funkcje wbudowane [#builtin]_
* brak określenia typu zmiennej (nazwy)
* brak średnika na końcu linii

**Uwaga!** Funkcja input() zawsze zwraca wartości typu napisowego (string).


.. [#builtin] https://docs.python.org/3/library/functions.html


Literatura
----------

1. `General Python FAQ <https://docs.python.org/3/faq/general.html>`__
2. `Python For Beginners <https://www.python.org/about/gettingstarted/>`__
