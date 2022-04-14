Python - Dekoratory
===================

.. note::

  Wszystkie przykłady zawarte w tym poście pisane są z myślą o Pythonie w wersji 3.6.

Dekoratory opisano w dwóch dokumentach — `PEP 318 <https://www.python.org/dev/peps/pep-0318/>`__ oraz `PEP 3129 <https://www.python.org/dev/peps/pep-3129>`__. Pierwszy z nich został opublikowany w 2003 roku (Python 2.4) i dotyczy dekoratorów stosowanych do funkcji oraz metod. Po 4 latach (rok 2007, Python 3.0) opublikowano drugi dokument, w którym rozszerzono ich możliwości o dekorowanie klas.

Dekorator to obiekt, który można wywołać jak funkcję (klasa lub funkcja). Obiekt ten jest wrapperem dla pierwotnego obiektu.

Zobaczmy to na przykładzie. Utwórzmy najprostszy dekorator — funkcję, która będzie zwracała przekazany jej obiekt:

.. code:: python

  def dekorator(obj):
      return obj

Opatrzmy teraz przykładową funkcję naszym nowo utworzonym dekoratorem:

.. code:: python

  @dekorator
  def funkcja():
      print("hello")

Zapis ze znakiem ``@`` przed funkcją to `syntactic sugar <https://pl.wikipedia.org/wiki/Lukier_sk%C5%82adniowy>`__ i jest on równoważny następującemu zapisowi::

  funkcja = dekorator(funkcja)

Operacje dokonywane są tutaj na nazwach. Nazwa ``funkcja`` przestaje wskazywać na obiekt reprezentujący naszą przykładową funkcję i od tego momentu wskazuje na obiekt zwrócony przez dekorator. W powyższym przypadku jest to ten sam obiekt, ale nietrudno jest sobie wyobrazić funkcję dekoratora w zmienionej postaci — zwracającej inny obiekt:

.. code:: python

  def inna_funkcja():
      print("inna funkcja")

  def dekorator(obj):
      return inna_funkcja

  @dekorator
  def funkcja():
      print("hello")

  funkcja()


Wynikiem działania powyższego skryptu jest::

  inna funkcja

Zgodnie z przedstawionym wcześniej równoważnym zapisem, nazwa ``funkcja`` wskazuje teraz na obiekt zwrócony przez dekorator — czyli ``inna_funkcja``.

Powszechną praktyką jest umieszczanie ``inna_funkcja`` w funkcji dekoratora i wywołanie w niej pierwotnego obiektu (w omawianym przypadku jest to ``funkcja``):

.. code:: python

  def dekorator(obj):
      def inna_funkcja():
          obj()
          print("world")
      return inna_funkcja
  
  @dekorator
  def funkcja():
      print("hello")
  
  funkcja()


Jednym z klasycznych już chyba przykładów na dekoratory jest ``cache``. Utworzymy dekorator o nazwie ``cache`` dla funkcji ``get_web_page`` zwracającej dane z serwisu internetowego:

.. code-block:: python
  :linenos:

  class WebMock():
      def get(self, url):
          return url + " always works!"
  
  def cache(wrapped_function):
      def wrapper(web, url):
          if url in "https://chyla.org/":
              return "It work's!"
          else:
              return wrapped_function(web, url)
      return wrapper
  
  @cache
  def get_web_page(web, url):
      return web.get(url)
  
  
  web = WebMock()
  
  page = get_web_page(web, "chyla.org")
  print("chyla.org content: " + page)
  
  page = get_web_page(web, "google.com")
  print("google.com content: " + page)


Odwołanie do zawartości zdalnej może chwilę potrwać, dlatego zamiast rzeczywistego połączenia stworzyłem klasę ``WebMock``. W przyszłości obiekt może zostać zmieniony, by faktycznie odwoływał się do treści umieszczonej w Internecie.

Na wydruku widzimy również funkcję ``cache`` będącą dekoratorem. Zwraca ona funkcję wrapper, która sprawdza, czy zna już podany adres i jeśli tak to zwraca wartość z cache, w przeciwnym wypadku wywołuje funkcję ``get_web_page`` odpowiedzialną za pobranie danych.

Pozostała część kodu powinna być dość oczywista. Jeśli nie, to zapraszam do dyskusji w komentarzach.


Przekazywanie argumentów
------------------------

Do dekoratora możemy przekazać dowolne argumenty. W tym celu wykorzystamy nową funkcję, zobaczmy fragment kodu:

.. code-block:: python
  :linenos:

  class WebMock():
      def get(self, url):
          return url + " always works!"
  
  def cache_with_value(cache_value):
      def cache(wrapped_function):
          def wrapper(web, url):
              if url in "https://chyla.org/":
                  return cache_value
              else:
                  return wrapped_function(web, url)
          return wrapper
      return cache
  
  @cache_with_value("It work's!")
  def get_web_page(web, url):
      return web.get(url)
  
  
  web = WebMock()
  
  page = get_web_page(web, "chyla.org")
  print("chyla.org content: " + page)
  
  page = get_web_page(web, "google.com")
  print("google.com content: " + page)

Trzeba przyznać, że ten kod niewiele różni się od poprzedniego. Funkcja ``cache``, widoczna w linii 6, jest prawie taka sama. Zmiana widoczna jest w linii 9, wykorzystywany jest parametr funkcji ``cache_with_value``.

Istotną zmianą jest dodanie wspomnianej funkcji ``cache_with_value``. Przyjmuje ona parametr i zwraca funkcję ``cache``. Spójrzmy na powiązaną z tym zmianę w linii 15, to jest wywołanie funkcji. W poprzednim przykładzie (linia 13) tego wywołania nie było. Ostatecznie w to miejsce zostanie wstawiona funkcja ``cache``.

Spróbujmy zapisać to podobnie jak poprzednio, bez nadmiernej ilości cukru składniowego::

  get_web_page = cache_with_value("It works!")(get_web_page)

W efekcie jest to równoważne::

  get_web_page = cache(get_web_page)

Technika ta jest szeroko wykorzystywana i warto ją znać.


Dekorator w formie klasy
------------------------

Do tej pory skupialiśmy się na dekoratorze jako funkcji, ale może on być też klasą. Zobaczmy zmodyfikowany pierwszy przykład:

.. code-block:: python
  :linenos:

  class WebMock():
      def get(self, url):
          return url + " always works!"
  
  class cache():
      def __init__(self, fun):
          self.fun = fun
  
      def __call__(self, web, url):
          if url in "https://chyla.org/":
              return "It work's!"
          else:
              return self.fun(web, url)
  
  @cache
  def get_web_page(web, url):
      return web.get(url)
  
  
  web = WebMock()
  
  page = get_web_page(web, "chyla.org")
  print("chyla.org content: " + page)
  
  page = get_web_page(web, "google.com")
  print("google.com content: " + page)


Zapiszmy fragment odpowiedzialny za dekorator bez cukru składniowego::

  get_web_page = cache(get_web_page)

Widzimy, że jest to wywołanie funkcji ``__init__``, czyli nazwa ``get_web_page`` będzie wskazywała na instancję klasy. Podczas próby wywołania instancji klasy jak funkcji, wywołana zostanie metoda ``__call__``.

Czy dekorator w formie klasy może przyjmować argumenty? Oczywiście, zobaczmy zmodyfikowany drugi przykład:

.. code-block:: python
  :linenos:

  class WebMock():
      def get(self, url):
          return url + " always works!"
  
  class cache_with_value():
      def __init__(self, cache_value):
          self.cache_value = cache_value
  
      def __call__(self, obj):
          def wrapper(web, url):
              if url in "https://chyla.org/":
                  return self.cache_value
              else:
                  return obj(web, url)
          return wrapper
  
  @cache_with_value("It work's!")
  def get_web_page(web, url):
      return web.get(url)
  
  
  web = WebMock()
  
  page = get_web_page(web, "chyla.org")
  print("chyla.org content: " + page)
  
  page = get_web_page(web, "google.com")
  print("google.com content: " + page)


Widzimy, że został wykonany zabieg podobny do opisywanego już wcześniej. Najpierw tworzymy instancję klasy, po czym używamy jej jako dekoratora. Za pomocą funkcji ``__init__`` możemy przekazać argumenty, natomiast wywołanie funkcji ``__call__`` spowoduje udekorowanie funkcji.

Zapiszmy to bez cukru składniowego::

  get_web_page = cache_with_value("It works!")(get_web_page)

Ciąg ``cache_with_value("It works!")`` to oczywiście wywołanie konstruktora obiektu, następnie na tym obiekcie wywoływana jest funkcja ``__calll__``, do której przekazywany jest obiekt ``get_web_page``. Widoczna tutaj sytuacja jest analogiczna, do omawianego wcześniej przekazywania parametrów za pomocą funkcji.


Dekorowanie klasy
-----------------

Dekorowanie klasy odbywa się w sposób analogiczny, do dotychczas omówionych. Jedyną różnicą jest fakt, iż nie dekorujemy funkcji, a klasę.

Zobaczmy przykład zaproponowany przez *theheadofabroom* na *stackoverflow*:

.. code-block:: python

  def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
      if class_ not in instances:
          instances[class_] = class_(*args, **kwargs)
      return instances[class_]
    return getinstance
  
  @singleton
  class MyClass(BaseClass):
    pass

Dlaczego to działa? Otóż rozpisując przykład, w kod pozbawiony cukru składniowego, otrzymujemy::

  MyClass = singleton(MyClass)

``MyClass`` wskazuje teraz na funkcję ``getinstance``, którą składniowo wywołujemy w ten sam sposób, w jaki tworzymy nowy obiekt klasy::

  my_class_instance = MyClass()

Funkcja ta sprawdza, czy dany obiekt już istnieje i go zwraca, w przeciwnym wypadku jest on tworzony.

Zauważmy, że pierwotna nazwa ``MyClass`` nie wskazuje na obiekt klasy, ale na specjalny typ reprezentujący klasę.


Dekorator wraps
---------------

Dla przejrzystości kodu, w poprzednich przykładach pominięto, istotny podczas tworzenia własnego dekoratora, dekorator ``wraps``. Jego pominięcie powoduje utratę metadanych dekorowanej funkcji (np. docstringa). Zalecane jest, by był on dodawany do tworzonych dekoratorów.

Oto przykłady, bazujące na tych z dokumentacji, pokazujące utratę metadanych.

Wersja z dekoratorem ``wraps``:

.. code:: python

  from functools import wraps
  
  def my_decorator(f):
      @wraps(f)
      def wrapper(*args, **kwds):
          print('Calling decorated function')
          return f(*args, **kwds)
      return wrapper
  
  @my_decorator
  def example():
      """Docstring"""
      print('Called example function')
  
  example()
  print(example.__name__)
  print(example.__doc__)


Wynik działania::

  Calling decorated function
  Called example function
  example
  Docstring

Wersja bez dekoratora ``wraps``:

.. code:: python

  def my_decorator(f):
      def wrapper(*args, **kwds):
          print('Calling decorated function')
          return f(*args, **kwds)
      return wrapper
  
  @my_decorator
  def example():
      """Docstring"""
      print('Called example function')
  
  example()
  print(example.__name__)
  print(example.__doc__)


Wynik działania::

  Calling decorated function
  Called example function
  wrapper
  None


Literatura
----------

1. `PEP 318 -- Decorators for Functions and Methods <https://www.python.org/dev/peps/pep-0318/>`__
2. `PEP 3129 -- Class Decorators <https://www.python.org/dev/peps/pep-3129/>`__
3. `Creating a singleton in Python <https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python>`__
4. `10.2. functools — Higher-order functions and operations on callable objects <https://docs.python.org/3.6/library/functools.html>`__
