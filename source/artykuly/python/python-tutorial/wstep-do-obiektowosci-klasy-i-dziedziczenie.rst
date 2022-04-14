Wstęp do obiektowości - Klasy i dziedziczenie
=============================================

.. pdfobject:: /_static/files/artykuly/python/python-tutorial/Wstep-do-obiektowosci-Klasy-i-dziedziczenie.pdf


Klasy
-----

Wprowadzenie
^^^^^^^^^^^^

Dotychczas koncentrowaliśmy się na zmienych oraz funkcjach. Stwórzmy funkcję, która wypisze podstawowe informacje o startującym samochodzie.

.. code-block:: python

    s1_kolor = 'czerwony'
    s1_marka = 'fiat'

    s2_kolor = 'czarny'
    s2_marka = 'bmw'

    def run(kolor, marka):
        print("Startuje", kolor, marka)

    run(s1_kolor, s1_marka)
    run(s2_kolor, s2_marka)


Jakie problemy możemy dostrzec w przytoczonym kodzie źródłowym?

1. Możliwa błędna kolejność podanych argumentów w funkcji run.
2. “Zmieszanie” dwóch różnych samochodów (np. kolor z s1, marka z s2).
3. Podanie dwa razy tych samych argumentów (np. marka zamiast koloru).

**Główny problem:**
**Poszczególne zmienne określające dany samochód nie są ze sobą w żaden sposób powiązane.**


Definicja Klasy
^^^^^^^^^^^^^^^

Korzystając z klas możemy powiązać poszczególne zmienne ze sobą.

**Definicja klasy (klasa) określa zachowanie i stan obiektu.**

Na podstawie definicji klasy tworzone są konkretne obiekty - instancje klasy.

.. code-block:: python

    class Samochod:
        pass

    def run(sam):
        print("Startuje", sam.kolor, sam.marka)

    s1 = Samochod()
    s1.kolor = 'czerwony'
    s1.marka = 'fiat'

    run(s1)


Metody klasy
^^^^^^^^^^^^

Co możemy poprawić w omawianym przykładzie?

Warto napisać dodatkową funkcję, która jako parametr będzie przyjmowała obiekt samochodu oraz atrybuty, które należy ustawić w przekazanym obiekcie. Stosując takie rozwiązanie nie pominiemy żadnego z atrybutów.

.. code-block:: python

    class Samochod:
        pass

    def run(sam):
        print("Startuje", sam.kolor, sam.marka)


    def init(sam, kolor, marka):
        sam.kolor = kolor
        sam.marka = marka

    s1 = Samochod()
    init(s1, 'czerwony', 'fiat')

    run(s1)


Nowa funkcja ``init()`` ustawia odpowiednie zmienne w **konkretnym** obiekcie samochodu.

Powiązaliśmy ze sobą zmienne, czy to samo możemy zrobić z funkcjami? Co się stanie jeśli wywołamy którąś z funkcji na obiekcie innej klasy niż samochód?


Funkcje związane z daną klasą możemy umieścić w jej definicji.

.. code-block:: python

    class Samochod:
        def run(self):
            print("Startuje", self.kolor, self.marka)


    def init(sam, kolor, marka):
        sam.kolor = kolor
        sam.marka = marka

    s1 = Samochod()
    init(s1, 'czerwony', 'fiat')

    s1.run()  # --- wcześniej --->   run(s1)


**Zwróćmy uwagę, że jedyny parametr funkcji zmienił swoją nazwę z ‘sam’ na ‘self’, wskazuje on instancję klasy.**

Nazwa tego parametru jest dowolna, jednak PEP 8 zaleca stosowanie nazwy ‘self’.

Zmienił się także sposób wywołania funkcji ``run()``. Pierwszy parametr funkcji znajduje się teraz z lewej strony.

Również funkcję ``__init__()`` możemy umieścić w definicji klasy. Funkcję taką nazywamy konstruktorem lub po prostu funkcją init. Ustawia ona początkowy stan obiektu.

.. code-block:: python

    class Samochod:
        def __init__(self, kolor, marka):
            self.kolor = kolor
            self.marka = marka

        def run(self):
            print("Startuje", self.kolor, self.marka)

    s1 = Samochod("czerwony", "fiat")
    s1.run()

Również w przypadku tej funkcji zmieniła się nazwa pierwszego parametru i sposób jej wywołania.


Dziedziczenie
-------------

Wprowadzenie
^^^^^^^^^^^^

Zmodyfikujmy lekko nasz przykład. Uwzględnijmy poziom paliwa, jakim dysponuje samochód i uzależnijmy od tego jego start.

Dla samochodu benzynowego stwórzmy klasę SamochodBenzyna.

.. code-block:: python

    class SamochodBenzyna:
        def __init__(self, kolor, marka, benzyna):
            self.kolor = kolor
            self.marka = marka
            self.benzyna = benzyna

        def run(self):
            if self.czy_mozna_wystartowac():
                print("Startuje",
                    self.kolor, self.marka)

        def czy_mozna_wystartowac(self):
            return self.benzyna > 10


Podobnie sytuacja będzie wyglądała dla samochodu na gaz. Stwórzmy klasę SamochodLPG z odpowiednimi polami, czyli zmiennymi klasy.

.. code-block:: python

    class SamochodLPG:
        def __init__(self, kolor, marka, lpg):
            self.kolor = kolor
            self.marka = marka
            self.lpg = lpg

        def run(self):
            if self.czy_mozna_wystartowac():
                print("Startuje",
                    self.kolor, self.marka)

        def czy_mozna_wystartowac(self):
            return self.lpg > 20

Czy możemy zrobić to lepiej?


Hierarchia klas
^^^^^^^^^^^^^^^

Pomysł:

Stwórzmy jedną ogólną definicję klasy samochód - uniwersalną dla każdego samochodu. Ogólna wersja nie zawiera pól i metod odpowiedzialnych za poziom paliwa.

.. code-block:: python

    class Samochod:  # klasa nadrzędna/bazowa
        def __init__(self, kolor, marka):
            self.kolor = kolor
            self.marka = marka

        def run(self):
            if self.czy_mozna_wystartowac():
                print("Startuje",
                    self.kolor, self.marka)

Na podstawie klasy Samochod stwórzmy klasę SamochodBenzyna przeznaczoną dla samochodów benzynowych.

**Klasa ta będzie zawierała wszystkie pola i metody klasy Samochód. Mechanizm ten nazywamy dziedziczeniem.**

Klasę po której dziedziczymy nazywamy klasą bazową, nowo tworzoną klasę nazywamy klasą pochodną.

.. code-block:: python

    class SamochodBenzyna(Samochod):  # klasa pochodna; Samochod - klasa po której dziedziczymy (bazowa)
        pass

    s1 = SamochodBenzyna('czerwony', 'fiat')


Obiekt utworzony na podstawie klasy SamochodBenzyna nie jest w pełni funkcjonalny. Zawiera on co prawda metodę ``run()``, jednak nigdzie nie została zdefiniowana metoda ``czy_mozna_wystartowac()``. Próba wywołania metody ``run()`` spowoduje błąd wykonania.

.. code-block:: python

    class SamochodBenzyna(Samochod):
        pass

    s1 = SamochodBenzyna('czerwony', 'fiat')
    s1.run()  # BŁĄD! brak metody czy_mozna_wystartowac

Uzupełnijmy definicję klasy SamochodBenzyna o potrzebne pola i metody. Tworzymy nowy konstruktor (funkcję ``__init__()``) uwzględniający pole benzyna, a także nową funkcję ``czy_można_wystartować()``.

.. code-block:: python

    class SamochodBenzyna(Samochod):
        def __init__(self, kolor, marka, benzyna):
            self.kolor = kolor
            self.marka = marka
            self.benzyna = benzyna

        def czy_mozna_wystartowac(self):
            return self.benzyna > 10

    s1 = SamochodBenzyna('czerwony', 'fiat', 15)
    s1.run()


Co można zrobić lepiej?

**Zasada DRY - Don't Repeat Yourself!**

Istniał już konstruktor, który potrafił ustawić pola kolor oraz marka.

Zamiast na nowo pisać kolejne instrukcje przypisania skorzystajmy z konstruktora dostępnego w klasie Samochod, zrobimy to przy pomocy funkcji ``super()``.

.. code-block:: python

    class SamochodBenzyna(Samochod):
        def __init__(self, kolor, marka, benzyna):
            super().__init__(kolor, marka)
            self.benzyna = benzyna

        def czy_mozna_wystartowac(self):
            return self.benzyna > 10


    s1 = SamochodBenzyna('czerwony', 'fiat', 15)
    s1.run()


Widoczność atrybutów
^^^^^^^^^^^^^^^^^^^^

Tworząc klasy musimy zadbać o widoczność pól i metod. Nie zawsze chcemy, by każde pole było dostępne do użytku poza metodami danej klasy. Zachowanie to nazywamy **hermetyzacją** lub inaczej **enkapsulacją**.

**Pole prywatne** - dostępne tylko dla metod danej klasy, tworzymy poprzez **dodanie znaku podkreślenia na początku nazwy**.

.. code-block:: python

    class Samochod:
        def __init__(self, kolor, marka):
            self.kolor = kolor  # pole publiczne
            self.marka = marka

        def run(self):
            if self._czy_mozna_wystartowac():  # wywołanie metody prywatnej
                print("Startuje",
                    self.kolor, self.marka)

Pola prywatne utworzone za pomocą jednego znaku podkreślenia są prywatne w rozumieniu umowy między programistami, określa to dokument PEP 8.

**Interpreter nie weryfikuje dostępu do pola/metody.**

.. code-block:: python

    class SamochodBenzyna(Samochod):
        def __init__(self, kolor, marka, benzyna):
            super().__init__(kolor, marka)
            self._benzyna = benzyna  # pole prywatne

        def _czy_mozna_wystartowac(self):
            return self._benzyna > 10


    s1 = SamochodBenzyna('czerwony', 'fiat', 15)
    s1.run()

Pola/metody prywatne można również utworzyć za pomocą **podwójnego znaku podkreślenia**. W takim przypadku **interpreter weryfikuje dostęp i powiadamia o błędzie**. Do takich pól/metod nie można odwołać się w klasie nadrzędnej (bazowej) i pochodnej.

Nazwy zaczynające się i kończące się dwoma znakami podkreślenia są funkcjami o specjalnym przeznaczeniu (przykład: funkcja ``__init__()``).


Atrybuty statyczne
^^^^^^^^^^^^^^^^^^

W definicji klasy możemy również umieścić pola i metody statyczne. Pole statyczne przyjmuje jedną wartość dla wszystkich instancji danej klasy. Pola/metody statyczne nie muszą byćwywoływane na konkretnym obiekcie danej klasy.

.. code-block:: python

    class Samochod:
        stala_mph_kph = 1.6093  # pole statyczne

        # ...

        @staticmethod
        def zamienMphNaKph(mile):  # funkcja statyczna
            return mile * Samochod.stala_mph_kph


    kph = Samochod.zamienMphNaKph(1)
    print('kph =', kph)


Literatura
----------

1. `A First Look at Classes <https://docs.python.org/3/tutorial/classes.html#a-first-look-at-classes>`__
2. `Private Variables <https://docs.python.org/3/tutorial/classes.html#private-variables>`__
3. `Inheritance <https://docs.python.org/3/tutorial/classes.html#inheritance>`__
4. `Staticmethod <https://www.programiz.com/python-programming/methods/built-in/staticmethod>`__
