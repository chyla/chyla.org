Rekurencja - Żeby zrozumieć rekurencję, najpierw musisz zrozumieć rekurencję
============================================================================

.. pdfobject:: /_static/files/artykuly/python/python-tutorial/Rekurencja.pdf


Rekurencja
----------

Rekurencja, zwana także rekursją – odwoływanie się np. funkcji lub definicji do samej siebie. [#rekurencja_wikipedia]_

Każda definicja rekurencyjna potrzebuje przynajmniej jednego przypadku bazowego (nie rekurencyjnego). W przeciwnym wypadku nigdy się nie zakończy (**warunek stopu**). [#rekurencja_wikipedia]_

*Innymi słowy:*
W pewnym momencie wywoływanie funkcji przez samą siebie musi się kiedyś zakończyć, dlatego potrzebny jest stan, w którym dana funkcja nie jest wywoływana ponownie.


.. [#rekurencja_wikipedia] https://pl.wikipedia.org/wiki/Rekurencja


Przykład - Suma kolejnych liczb całkowitych
-------------------------------------------

**W matematyce**::

	f(0) = 0
	f(n) = n + f(n - 1) 


Rozwinięcie::

	f(5) = 5 + f(5 - 1)
		 = 5 + f(4) = 5 + (4 + f(4 - 1)) 
		 = 5 + (4 + f(3)) = 5 + (4 + (3 + f(3 - 1)))
		 = 5 + (4 + (3 + f(2))) = 5 + (4 + (3 + (2 + f(2 - 1))))
		 = 5 + (4 + (3 + (2 + f(1))) = 5 + (4 + (3 + (2 + (1 + f(1 - 1)))))
		 = 5 + (4 + (3 + (2 + (1 + f(0)))) = 5 + (4 + (3 + (2 + (1 + 0))))
		 = 15


To samo zapisane **w języku Python**:

.. code-block:: python

	def f(n):
		if n == 0:   # <-- warunek stopu
			return 0
		else:
			return n + f(n - 1)

	x = f(5)

	print(x)

Rozwinięcie dla języka Python::

	x = f(5)
	  = 5 + f(5 - 1)
	  = 5 + f(4) = 5 + (4 + f(4 - 1)) 
	  = 5 + (4 + f(3)) = 5 + (4 + (3 + f(3 - 1)))
	  = 5 + (4 + (3 + f(2))) = 5 + (4 + (3 + (2 + f(2 - 1))))
	  = 5 + (4 + (3 + (2 + f(1))) = 5 + (4 + (3 + (2 + (1 + f(1 - 1)))))
	  = 5 + (4 + (3 + (2 + (1 + f(0)))) = 5 + (4 + (3 + (2 + (1 + 0))))
	  = 5 + (4 + (3 + (2 + (1)))
	  = 5 + (4 + (3 + (3)))
	  = 5 + (4 + (6))
	  = 5 + (10)
	  = 15


Przykład - Ciąg Fibonacciego
----------------------------

**W matematyce**::

	F(0) = 0
	F(1) = 1
	F(n) = F(n-1) + F(n-2)


To samo zapisane **w języku Python**:

.. code-block:: python

	def F(n):
		if n == 0:  # <-- warunek stopu
			return 0
		elif n == 1: # <-- warunek stopu
			return 1
		else:
			return F(n - 1) + F(n - 2)


.. important::

	Obliczenia wykonywane rekurencyjnie **nie zawsze są efektywne**.

	Obliczenia rekurencyjne często wymagają większej liczby wykonywanych obliczeń, a także wiążą się ze zwiększonym wykorzystaniem pamięci.


Literatura
----------

1. `Rekurencja, Education in Mathematics and Computing, Uniwersytet w Waterloo <https://cscircles.cemc.uwaterloo.ca/16-pl/>`__
2. `Rekurencja, Paweł Kłeczek <http://home.agh.edu.pl/~pkleczek/dokuwiki/doku.php?id=dydaktyka:aisd:2016:recursion>`__
