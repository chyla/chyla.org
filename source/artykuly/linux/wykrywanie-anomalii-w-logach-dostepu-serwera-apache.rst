Wykrywanie anomalii w logach dostępu serwera Apache
===================================================

Artykuł opisuje metodę przedstawioną w „Detecting anomalous Web server usage through mining access logs” T. Gržinić, T. Kišasondi, J. Šaban. Szczególne podziękowania należą się Panu Toni Gržinić, który odpowiedział na pytania dotyczące pracy.

Przykłady do każdego omawianego kroku znajdują się w prezentacji:

.. pdfobject:: /_static/files/artykuly/linux/Wykrywanie-anomalii-w-logach-dostepu-do-serwera-Apache-za-pomoca-algorytmu-KNN.pdf

Zakładamy, że dysponujemy tylko zawartością pliku logów dostępu do serwera (`access log <https://httpd.apache.org/docs/2.4/logs.html>`_). Metoda opiera się na analizie wysłanych zapytań przez jednego użytkownika, sesję. Jeśli któraś sesja za bardzo odbiega od pozostałych (np. pod względem liczby wysłanych zapytań do serwera, rozmiaru zapytań) jest ona traktowana jako anomalia, może być wynikiem działania atakującego. Do wstępnego określenia, czy sesje są wynikiem normalnego ruchu, czy anomalią zastosować możemy metodę IQR. Wyniki uzyskane metodą IQR należy prawdopodobnie poprawić, nie każda sesja z dużą ilością zapytań musi być związana z atakiem.


Metoda rozstępu międzykwartylowego
----------------------------------

Metoda rozstępu międzykwartylowego używana jest do określenia obserwacji odstających (anomalii) spośród podanego posortowanego niemalejąco zbioru liczb (tutaj ilości zapytań).

Polega na:

* obliczeniu różnicy (IQR) pomiędzy kwartylem trzecim (Q3) a kwartylem pierwszym (Q1)
* oznaczeniu wszystkich wartości mniejszych od Q1 – 1.5 * IQR jako wartości odstających
* oznaczeniu wszystkich wartości większych od Q3 + 1.5 * IQR jako wartości odstających


Wyodrębnienie sesji użytkowników
--------------------------------

Na podstawie wpisów (reprezentujących zapytania) w logach należy wyróżnić poszczególne sesje użytkownika. Do wykonania tego zadania zostanie wykorzystany:

* znacznik czasu (timestamp)
* adres IP
* Identyfikator przeglądarki (user-agent)
* Zakładamy, że sesja użytkownika nie trwa dłużej, niż godzinę. Jeśli zapytania zawierają ten sam adres IP oraz identyfikator klienta (user-agent) należą one do tej samej sesji.


Obliczenie statystyk
--------------------

Dla każdej sesji należy obliczyć statystyki zawierające:

* czas trwania sesji (różnica czasu pomiędzy ostatnim a pierwszym zapytaniem w sesji w sekundach)
* użycie pasma sieciowego (ilości pobranych danych w bajtach) całkowita liczba zapytań w danej sesji
* procent błędnych zapytań (kod błędu jest pomiędzy 400 a 500)


Oznaczenie sesji jako anomalii
------------------------------

Mając statystyki dotyczące każdej sesji możemy próbować wyznaczyć anomalie metodą IQR. Oczywiście oprócz ilości zapytań można brać pod uwagę dowolny inny element statystyki (np. użycie pasma, czy procent błędnych zapytań). Tak oznaczone sesje należy przejrzeć i ewentualnie poprawić ich klasyfikację. Oznaczanie sesji jako anomalii metodą IQR jest tylko pewnym przybliżeniem.


Analiza danych za pomocą algorytmu kNN
--------------------------------------

Algorytm K-najbliższych sąsiadów (K-nearest neighbours) służy do kategoryzacji nowych obserwacji na podstawie znanych obserwacji i ich kategorii. Jako znane obserwacje traktujemy wyliczone wcześniej statystyki wraz z ich oznaczeniem (anomalia, czy nie). Obserwacje (statystyki sesji) do kategoryzacji powstaną na podstawie logów, które zostaną wygenerowane w przyszłości.

Nowe obserwacje (statystyki) z łatwością będą mogły być rozpoznane jako anomalia, bądź nie. Zamiast algorytmu kNN można wykorzystać sieci neuronowe, lasy losowe i inne algorytmy pozwalające na kategoryzację.


Literatura
----------

1. `Sztuczna inteligencja; Algorytm kNN <http://www.tomaszx.pl/materialy/si_lab7.pdf>`_
2. `„Detecting anomalous Web server usage through mining access logs” T. Gržinić, T. Kišasondi, J. Šaban <http://archive.ceciis.foi.hr/app/public/conferences/1/papers2013/627.pdf>`_
