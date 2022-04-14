Zmienne środowiskowe w systemie Linux
=====================================

Zmienne środowiskowe to dodatkowe dane przekazywane do uruchamianego programu. Ustawiane  są  podczas  uruchamiania  systemu,  procesu  logowania  użytkownika oraz w trakcie pracy powłoki systemowej.

Zmienne te zawierają informacje takie jak:

 * aktualny katalog roboczy (CWD, zmienna PWD),
 * wykorzystywany interpreter języka poleceń (zmienna SHELL),
 * położenie katalogu domowego użytkownika (zmienna HOME),
 * katalogi, w których poszukiwane są programy (zmienna PATH).


.. pdfobject:: /_static/files/artykuly/linux/Zmienne-srodowiskowe-w-systemie-Linux-Przekazywanie-danych-do-programu.pdf


Zmienne środowiskowe w języku C
-------------------------------

Zmienne środowiskowe przechowywane są jako napisy postaci `NAZWA=WARTOŚĆ` w globalnej tablicy `environ`.

Do operacji na zmiennych środowiskowych służą funkcje:  `getenv()`, `putenv()`, `setenv()`, `unsetenv()`.

.. code:: c

  #include <stdio.h>

  extern char **environ;

  int main() {
      char **env = environ;

      while (*env != NULL) {
          printf("%s\n", *env);
          env++;
      }

      return 0;
  }


Zmienne środowiskowe w powłoce BASH
-----------------------------------

Domyślnie zmienne powłoki nie są przekazywane do podprocesów i są widoczne jedynie w bieżącej powłoce. Zmienną taką należy wyeksportować, aby stała się widoczna dla procesu potomnego jako zmienna środowiskowa.

Przyjęło się, że nazwy zmiennych środowiskowych (eksportowane zmienne powłoki) pisane są wielkimi literami, chociaż są od tego wyjątki (np. `http_proxy`).

Do wyświetlenia wszystkich zmiennych powłoki można wykorzystać polecenie `set`, natomiast do wyświetlenia zmiennych środowiskowych polecenia `env` oraz `printenv`.

.. code:: sh

  $ LC_ALL=C
  $ printenv | grep LC_ALL
  $ set | grep LC_ALL
  LC_ALL=C
  $ export LC_ALL
  $ printenv | grep LC_ALL
  LC_ALL=C
  $ set | grep LC_ALL
  LC_ALL=C

Więcej informacji i przykładów znajdziesz w prezentacji umieszczonej na górze strony.


Literatura
----------

1. `EnvironmentVariables <https://help.ubuntu.com/community/EnvironmentVariables>`__
2. `Zmienne środowiskowe <https://web.archive.org/web/20170501173703/http://www.turox.org.pl/podrecznik/Zmienne_srodowiskowe.html>`__
3. `man 1 bash <https://linux.die.net/man/1/bash>`__
4. `man 7 environ <https://linux.die.net/man/7/environ>`__
5. `man 3 getenv <https://linux.die.net/man/3/getenv>`__
6. `man 3 putenv <https://linux.die.net/man/3/putenv>`__
7. `man 3 setenv <https://linux.die.net/man/3/setenv>`__
8. `man 3 unsetenv <https://linux.die.net/man/3/unsetenv>`__

