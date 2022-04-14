Jak poprawnie wywołać funkcję C++ z języka C?
=============================================

Pewnie większość z nas wie, że `extern "C"` (`language linkage <https://en.cppreference.com/w/cpp/language/language_linkage>`__) wyłącza dekorowanie nazw funkcji (ang. `name mangling <https://en.wikipedia.org/wiki/Name_mangling>`__) i ustawia `external linkage <https://en.cppreference.com/w/cpp/language/storage_duration>`__. Kompilator C++ dodaje dodatkowe napisy do nazwy na potrzeby, chociażby, `przeciążania funkcji <https://pl.wikipedia.org/wiki/Przeci%C4%85%C5%BCanie_funkcji>`__.

  A mangled name encodes a function or
  variable's name, scope, type, and/or template arguments into a text
  identifier.  This identifier is used as the function's or
  variable's linkage name, to preserve compatibility between C++'s
  language features (*templates, scoping, and overloading*) and C
  linkers.

  (źródło: `github.com/gcc-mirror/gcc <https://github.com/gcc-mirror/gcc/blob/master/gcc/cp/mangle.c>`__)

Zobaczmy przykład:

.. code-block:: cpp

  void moja_funkcja(int, int) {}

  int moja_funkcja(char) {}

  int main() {}


A oto wygenerowane symbole (pominąłem nieistotne)::

  00000000000006a9 T main
  000000000000069d T _Z12moja_funkcjac
  0000000000000690 T _Z12moja_funkcjaii

Pierwsza funkcja otrzymała nazwę `_Z12moja_funkcjaii`, natomiast druga `_Z12moja_funkcjac`. Sposób dekorowania nazw jest zależny od kompilatora.

Kompilator języka C nie stosuje dekorowania nazw, nazwy używane w kodzie źródłowym są identyczne z nazwami wygenerowanych symboli. Zobaczmy to na kolejnym przykładzie:

.. code-block:: c

  void inna_funkcja(int a, int b) {}

  int main() {}

Wygenerowane symbole (tutaj także pominąłem nieistotne)::

  0000000000000660 T inna_funkcja
  000000000000066d T main

Dekorowanie nazw uniemożliwia linkowanie z kodem wynikowym wygenerowanym za pomocą kompilatora języka C. Jak linkować funkcję języka C++, której nazwa w tablicy symboli jest zależna od kompilatora? Rozwiązaniem jest użycie `extern "C"`:

.. code-block:: cpp

  extern "C" void moja_funkcja(int, int) {}

  extern "C" int moja_druga_funkcja(char) {}

  int main() {}

Nazwa jednej z przykładowych funkcji musiała ulec zmianie, gdyż nie mogą istnieć dwie takie same nazwy w tablicy symboli::

  00000000000006a9 T main
  000000000000069d T moja_druga_funkcja
  0000000000000690 T moja_funkcja

Bazując na tych informacjach możemy bez problemu napisać program w języku C wywołujący funkcję języka C++.

Plik `funkcja.cpp`:

.. code-block:: cpp

  extern "C" void funkcja() {}


Plik `main.c`:

.. code-block:: cpp

  extern void funkcja();

  int main() {
    funkcja();
    return 0;
  }


A gdyby tak funkcja C przyjmowała adres na funkcję?
---------------------------------------------------

Spójrzmy na przykład.

Plik `funkcja.c`:

.. code-block:: cpp

  void funkcja( void (*ptr)() ) {
    ptr();
  }

Plik `main.cpp`:

.. code-block:: cpp

  extern "C" void funkcja( void (*ptr)() );

  void przekazywana() {}

  int main() {
    funkcja(&przekazywana);
  }

Główny kod programu znajduje się w pliku `main.cpp` kompilowany kompilatorem dla języka C++. Funkcja main() wywołuje `funkcja` z pliku `funkcja.c` kompilowanym kompilatorem języka C. `funkcja` wywołuje funkcję przekazaną jako argument. W tym przykładzie nie ma problemów z linkowaniem.

Problem w tym, że kod źródłowy z pliku `funkcja.c` jest kodem źródłowym języka C i zapis `ptr()` wywołuje funkcję przekazaną jako argument tak, jak zwykłą funkcję języka C. Przekazywana funkcja jest natomiast funkcją języka C++ i oczekuje, że będzie wywołana tak jak funkcja języka C++.

Mówiąc precyzyjniej problem dotyczy zgodności `konwencji wywołań funkcji <https://en.wikipedia.org/wiki/Calling_convention>`__ C i C++. Dla języka C++ mogła (ale nie musiała) zostać przyjęta inna konwencja niż dla języka C.

Problem rozwiąże dodanie `extern "C"` do definicji funkcji `przekazywana()`. Na tej podstawie kompilator C++ będzie wiedział jakiej konwencji wywołań użyć:

  Every function type, every function name with external linkage, and every variable name with external linkage, has a property called language linkage. Language linkage encapsulates the set of requirements necessary to link with a module written in another programming language: **calling convention, name mangling algorithm, etc.**

  (źródło: `cppreference.com <https://en.cppreference.com/w/cpp/language/language_linkage>`__)

Poprawiony przykład z użyciem `extern "C"`:

Plik `funkcja.c`:

.. code-block:: cpp

  void funkcja( void (*ptr)() ) {
    ptr();
  }

Plik `main.cpp`:

.. code-block:: cpp

  extern "C" void funkcja( void (*ptr)() );

  extern "C" void przekazywana() {}

  int main() {
    funkcja(&przekazywana);
  }

Na tego typu problem natkniemy się wykorzystując funkcje języka C, możemy do nich zaliczyć funkcje systemowe (np. te związane z pthreads).


Literatura
----------

1. `Language linkage <https://en.cppreference.com/w/cpp/language/language_linkage>`__
2. `How to mix C and C++ <https://isocpp.org/wiki/faq/mixing-c-and-cpp>`__
3. `What is function name mangling in programming and why it happens? <https://www.quora.com/What-is-function-name-mangling-in-programming-and-why-it-happens>`__
4. `Storage class specifiers <https://en.cppreference.com/w/cpp/language/storage_duration>`__
5. `Calling convention <https://en.wikipedia.org/wiki/Calling_convention>`__
