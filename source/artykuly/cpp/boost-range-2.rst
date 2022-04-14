Boost - Range 2.0
=================

Spis treści
-----------

1. Wstęp

   * przyszłość biblioteki Range
   * wprowadzenie do zakresów

2. Algorytmy

3. Adaptery


Wstęp
-----

Obecnie w C++ dostępne są zakresy dostarczane przez jedną z zestawu bibliotek Boost - Range v2, jednak nie nadążyła ona za szybkimi zmianami w standardzie. Jej udoskonalona wersja (v3) wykorzystuje nowe elementy języka, co podkreślają jej twórcy [3]:

    Why does C++ need another range library? Simply put, the existing solutions haven't kept up with the rapid evolution of C++. Range v3 is a library for the future C++. Not only does it work well with today's C++ -- move semantics, lambdas, automatically deduced types and all -- it also anticipates tomorrow's C++ with Concepts.

Twórcy Range v3 dokładają wszelkich starań, aby obsługa zakresów weszła do standardu [3]:

    Range v3 forms the basis of a proposal to add range support to the standard library (N4128: Ranges for the Standard Library). It also will be the reference implementation for an upcoming Technical Specification. These are the first steps toward turning ranges into an international standard.

Wersja trzecia może pojawić się w C++20 [5]. Aktualnie do wyboru mamy zakresy dostarczane w ramach biblioteki Boost Range [1] oraz wersję referencyjną range-v3 dostępną na GitHubie [3]. W tym artykule **skupię się na bibliotece Range v2**.

W swoim zamyśle zakresy są bardzo podobne do kontenerów STL, jednak nie muszą one być właścicielami elementów, ani obsługiwać operacji kopiowania. O zakresie możemy myśleć jak o obiekcie dostarczającym:

* iterator do pierwszego elementu
* iterator wskazujący za ostatni element
* liczbę dostępnych elementów

Definicję zakresu dobrze omówiono w dokumentacji [6]:

    A Range is a concept similar to the STL Container concept. A Range provides iterators for accessing a half-open range [first,one_past_last) of elements and provides information about the number of elements in the Range. However, a Range has fewer requirements than a Container.

    The motivation for the Range concept is that there are many useful Container-like types that do not meet the full requirements of Container, and many algorithms that can be written with this reduced set of requirements. In particular, a Range does not necessarily

    * own the elements that can be accessed through it,
    * have copy semantics,

    Because of the second requirement, a Range object must be passed by (const or non-const) reference in generic code.

Zobaczmy fragment głównej klasy szablonowej reprezentującej zakres [7]:

.. code-block:: cpp

  template< class ForwardTraversalIterator >
  class iterator_range
  {
  public: // Forward Range types
      typedef ForwardTraversalIterator   iterator;
      typedef ForwardTraversalIterator   const_iterator;
      typedef iterator_difference<iterator>::type difference_type;

  public: // construction, assignment
      template< class ForwardTraversalIterator2 >
      iterator_range( ForwardTraversalIterator2 Begin, ForwardTraversalIterator2 End );

      template< class ForwardRange >
      iterator_range( ForwardRange& r );

      template< class ForwardRange >
      iterator_range( const ForwardRange& r );

      template< class ForwardRange >
      iterator_range& operator=( ForwardRange& r );

      template< class ForwardRange >
      iterator_range& operator=( const ForwardRange& r );

  public: // Forward Range functions
      iterator  begin() const;
      iterator  end() const;

  public: // convenience
      operator    unspecified_bool_type() const;
      bool        equal( const iterator_range& ) const;
      value_type& front() const;
      void        drop_front();
      void        drop_front(difference_type n);
      bool      empty() const;

      iterator_range& advance_begin(difference_type n);
      iterator_range& advance_end(difference_type n);

      // for Bidirectional:
      value_type& back() const;
      void drop_back();
      void drop_back(difference_type n);
      // for Random Access only:
      reference operator[]( difference_type at ) const;
      value_type operator()( difference_type at ) const;
      size_type size() const;
  };


Zawarte zostały w niej metody ``begin()`` oraz ``end()`` zwracające odpowiednio iterator do pierwszego elementu oraz iterator wskazujący za ostatni element. U dołu definicji klasy znajdziemy również metodę ``size()`` zwracającą ilość elementów w zakresie. Dostępnych jest także kilka konstruktorów pozwalających na stworzenie zakresu, chociaż najciekawszym jest pierwszy z nich. Warto zauważyć, że dostępność poszczególnych metod zależy od typu iteratora stosowanego podczas tworzenia instancji klasy.

W świetle powyższej definicji **kontenery z biblioteki standardowej są również zakresami**.


Algorytmy
---------

Biblioteka dostarcza algorytmy współpracujące z zakresami [8]. Głównie są to odmiany algorytmów (nie wszystkich) znanych z biblioteki standardowej, chociaż znajdzie się także kilka nowych [9]. Różnicą pomiędzy wersją z STL a wersją z Boost Range są parametry wejściowe - algorytmy biblioteki standardowej operują na iteratorach, natomiast biblioteka Range na zakresach.

Zobaczmy to na przykładzie funkcji ``sort()`` - w liniach 1-2 wersja z STL [9], a w liniach 4-5 wersja z biblioteki Range [10]:

.. code-block:: cpp

  template< class RandomIt >
  void sort( RandomIt first, RandomIt last );

  template<class RandomAccessRange>
  RandomAccessRange& sort(RandomAccessRange& rng);

Oczywiście nie może zabraknąć przykładu wykorzystania danej metody:

.. code-block:: cpp

  #include <algorithm>
  #include <iostream>
  #include <vector>

  #include <boost/range/algorithm/sort.hpp>

  using namespace std;

  int main()
  {
      vector<int> example_range { 4, 2, 3, 1 };

      // std::sort(example_range.begin(), example_range.end());
      boost::sort(example_range);

      for (auto i : example_range)
          cout << i << " ";
  }

Na powyższym wydruku możemy zaobserwować, że wersję operującą na zakresach cechuje zwięzłość. Zachęcam do zapoznania się z `dostępnymi algorytmami <http://www.boost.org/doc/libs/1_65_1/libs/range/doc/html/range/reference/algorithms.html>`__ np.:

* `fill <http://www.boost.org/doc/libs/1_64_0/libs/range/doc/html/range/reference/algorithms/mutating/fill.html>`__
* `generate <http://www.boost.org/doc/libs/1_64_0/libs/range/doc/html/range/reference/algorithms/mutating/generate.html>`__
* `remove <http://www.boost.org/doc/libs/1_64_0/libs/range/doc/html/range/reference/algorithms/mutating/remove.html>`__
* `replace <http://www.boost.org/doc/libs/1_64_0/libs/range/doc/html/range/reference/algorithms/mutating/replace.html>`__
* `reverse <http://www.boost.org/doc/libs/1_64_0/libs/range/doc/html/range/reference/algorithms/mutating/reverse.html>`__
* `transform <http://www.boost.org/doc/libs/1_64_0/libs/range/doc/html/range/reference/algorithms/mutating/transform.html>`__
* `count <http://www.boost.org/doc/libs/1_64_0/libs/range/doc/html/range/reference/algorithms/non_mutating/count.html>`__
* `search <http://www.boost.org/doc/libs/1_64_0/libs/range/doc/html/range/reference/algorithms/non_mutating/search.html>`__
* `insert <http://www.boost.org/doc/libs/1_64_0/libs/range/doc/html/range/reference/algorithms/new/insert.html>`__
* `for_each <http://www.boost.org/doc/libs/1_64_0/libs/range/doc/html/range/reference/algorithms/new/for_each.html>`__

Adaptery
--------

Adapter (ang. adaptor) jest klasą opakowującą istniejący zakres w nowy zakres. Jak zwykle dokumentacja jest nieoceniona [11]:

    A Range Adaptor is a class that wraps an existing Range to provide a new Range with different behaviour. Since the behaviour of Ranges is determined by their associated iterators, a Range Adaptor simply wraps the underlying iterators with new special iterators.

Zobaczmy przykład z użyciem adaptera ``filtered()``:

.. code-block:: cpp

  #include <iostream>
  #include <vector>

  #include <boost/range/adaptor/filtered.hpp>

  using namespace std;

  bool is_even(int x)
  {
      return x % 2 == 0;
  }

  int main()
  {
      vector<int> example_range { 1, 2, 3, 4 };

      for (auto i : example_range | boost::adaptors::filtered(is_even))
          cout << i << " ";
  }

Zapis ``example_range | boost::adaptors::filtered(is_even)`` jest adekwatny do wywołania funkcji, podobnie jak zaprezentowano to na poniższym wydruku:

.. code-block:: cpp

  #include <iostream>
  #include <vector>

  #include <boost/range/adaptor/filtered.hpp>

  using namespace std;

  bool is_even(int x)
  {
      return x % 2 == 0;
  }

  int main()
  {
      vector<int> example_range { 1, 2, 3, 4 };

      for (auto i : boost::adaptors::filter(example_range, is_even))
          cout << i << " ";
  }

Wynik działania obu programów::

    2 4

Funkcja ``filter()`` pobiera zakres oraz predykat, a zwraca nowy zakres zawierający iterator, który w trakcie odpytywania przeszukuje wektor w poszukiwaniu elementu spełniającego predykat.

Koncepcyjnie klasę filtered oraz jej iterator możemy przedstawić następująco:

.. code-block:: cpp

  struct filtered : Range
  {
      PredIterator begin;
      PredIterator end;

      filtered(Range range, Predicate pred) :
        begin(range.begin(), range.end(), pred),
        end(range.end(), range.end(), pred)
      {}

      // ...
  }

  struct PredIterator
  {
      Iterator begin;
      Iterator end;
      Predicate pred;

      PredIterator(Iterator begin, Iterator end, Predicate pred) :
        begin(begin), end(end), pred(pred)
      {}

      // ...

      PredIterator oprtator++() 
      {
          auto it = begin;
          while (it != end)
          {
              if (pred(*it) == true)
                  break;
              it++;
          }
          return PredIterator(it, end, pred);
      }
  }


  filtered filter(Range range, Predicate pred)
  {
      return filtered(range, pred);
  }

Powyższy pseudokod jest zwięzłym opisem implementacji zawartej w pliku `filtered.hpp <https://github.com/boostorg/range/blob/4a80ccd50d1348d602297c93d2f19fcf103a519d/include/boost/range/adaptor/filtered.hpp>`__.

W liniach 1 - 9 zaprezentowano pseudokod klasy ``filtered()`` - jest to zakres zawierający specjalny iterator, który będzie użyty do odpytywania kolejnych elementów.

W liniach 14 - 37 przedstawiono pseudokod iteratora - metoda ``operator++`` zwraca iterator do elementu dla którego spełniony został warunek lub iterator końca.

Należy zauważyć, że zakresy działają w oparciu o iteratory, dlatego ważne jest aby element na którym wykonują pracę istniał w trakcie operacji zakresowych. Zobaczmy to na przykładzie:

.. code-block:: cpp

  #include <iostream>
  #include <vector>

  #include <boost/range/adaptor/filtered.hpp>

  using namespace std;

  bool is_even(int x)
  {
      return x % 2 == 0;
  }

  int main()
  {
      vector<int> example_range { 1, 2, 3, 4 };

      auto rng = boost::adaptors::filter(example_range, is_even);

      example_range = vector<int>();

      for (auto i : rng) // błąd! zakres rng będzie odwoływał się do obiektu
      {                  // z linii 15, a ten został usunięty (linia 19)
          cout << i << " ";
      }
  }

Podobnie wygląda to z obiektami tymczasowymi:

.. code-block:: c

  #include <iostream>
  #include <vector>

  #include <boost/range/adaptor/filtered.hpp>

  using namespace std;

  bool is_even(int x)
  {
      return x % 2 == 0;
  }

  int main()
  {
      auto rng = boost::adaptors::filter(std::vector<int>{1, 2, 3, 4}, is_even);

      for (auto i : rng) // błąd! zakres rng będzie odwoływał się do obiektu tymczasowego std::vector<int>{1, 2, 3, 4}
      {                  // a ten już nie istnieje (obiekt filter zachował tylko iteratory, a nie cały obiekt)
          cout << i << " ";
      }
  }

Zachęcam do zapoznania się z `pozostałymi adapterami <http://www.boost.org/doc/libs/1_65_1/libs/range/doc/html/range/reference/adaptors/reference.html>`__ np.:

* `copied <http://www.boost.org/doc/libs/1_65_1/libs/range/doc/html/range/reference/adaptors/reference/copied.html>`__
* `replaced <http://www.boost.org/doc/libs/1_65_1/libs/range/doc/html/range/reference/adaptors/reference/replaced.html>`__
* `reversed <http://www.boost.org/doc/libs/1_65_1/libs/range/doc/html/range/reference/adaptors/reference/reversed.html>`__
* `sliced <http://www.boost.org/doc/libs/1_65_1/libs/range/doc/html/range/reference/adaptors/reference/sliced.html>`__
* `strided <http://www.boost.org/doc/libs/1_65_1/libs/range/doc/html/range/reference/adaptors/reference/strided.html>`__
* `transformed <http://www.boost.org/doc/libs/1_65_1/libs/range/doc/html/range/reference/adaptors/reference/transformed.html>`__

 
Literatura
----------

1. `Chapter 1. Range 2.0 <http://www.boost.org/doc/libs/1_65_1/libs/range/doc/html/index.html>`__
2. `Chapter 30. Boost.Range <https://theboostcpplibraries.com/boost.range>`__
3. `Biblioteka range-v3 <https://github.com/ericniebler/range-v3>`__
4. `Ranges for the Standard Library, Revision 1 <http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2014/n4128.html>`__
5. `C++20 (Wikipedia) <https://en.wikipedia.org/wiki/C%2B%2B20>`__
6. `Range 2.0: Overview <http://www.boost.org/doc/libs/1_65_1/libs/range/doc/html/range/concepts/overview.html>`__
7. `Range 2.0: Class iterator_range <http://www.boost.org/doc/libs/1_65_1/libs/range/doc/html/range/reference/utilities/iterator_range.html>`__
8. `Range 2.0: Range Algorithms <http://www.boost.org/doc/libs/1_65_1/libs/range/doc/html/range/reference/algorithms.html>`__
9. `std::sort <http://en.cppreference.com/w/cpp/algorithm/sort>`__
10. `Range 2.0: sort <http://www.boost.org/doc/libs/1_65_1/libs/range/doc/html/range/reference/algorithms/mutating/sort.html>`__
11. `Range 2.0: Adaptor - Introduction and motivation <http://www.boost.org/doc/libs/1_65_1/libs/range/doc/html/range/reference/adaptors/introduction.html>`__
