GDB - Tutorial
==============

.. note::

    Wszystkie prezentowane w artykule kody źródłowe dostępne są w repozytorium GitHub: https://github.com/chyla/GdbTutorial


Spis treści
-----------

1. Wstęp
2. Przygotowanie oprogramowania do pracy z GDB

   * kompilacja programu z dodatkowymi symbolami
   * osobny plik z symbolami

3. Uruchomienie aplikacji pod nadzorem GDB

   * uruchomienie z dodatkowymi symbolami
   * uruchomienie ze zrzutem pamięci
   * podłączenie do procesu

4. Debugowanie aplikacji

   * ustawienie pułapek
   * punkt obserwacji (obserwacja zmiennych)
   * usuwanie pułapek i punktów obserwacji
   * polecenia nawigacji
   * ustawienie oraz wyświetlenie zmiennych
   * obsługa wielowątkowości

5. Tekstowy interfejs użytkownika


Wstęp
-----

GDB (GNU Project Debugger) to najpopularniejsze narzędzie odpluskwiania (ang. debugging) w środowisku uniksowym. Pozwala monitorować wykonywany program oraz analizować przyczyny jego awarii. [1]

Omawiany debugger nie posiada graficznego interfejsu użytkownika, a jego obsługa sprowadza się do wykonywania odpowiednich poleceń w konsoli. Wiele środowisk programistycznych (np. `Code::Blocks <http://www.codeblocks.org/>`__, `CodeLite <https://codelite.org/>`__) integruje możliwości GDB, istnieją także niezależne projekty dostarczające graficzny interfejs użytkownika (np. `GNU DDD <https://www.gnu.org/software/ddd/>`__).

Wspierane są następujące języki programowania: C, C++, D, Go, Objective-C, Fortran, OpenCL C, Pascal, Rust, assembly, Modula-2 i Ada [2]. W wersji 8 i nowszych zrezygnowano z obsługi aplikacji Java kompilowanych z użyciem GNU Compiler for the Java Programming Language (GCJ) [3] – wiąże się to z faktem usunięcia GCJ z GNU Compiler Collection (GCC) 7 [4].


Przygotowanie oprogramowania do pracy z GDB
-------------------------------------------

Podczas kompilacji aplikacji mogą zostać wygenerowane symbole, czyli dodatkowe informacje przeznaczone dla debuggera. Mogą to być między innymi dane na temat zmiennych, funkcji, odpowiednich numerów linii w pliku źródłowym, czy użytym języku programowania [5,6]. Na ich podstawie debugger pozwala odwoływać się do poszczególnych elementów programu w przystępny sposób. Symbole mogą zostać umieszczone razem z programem w jednym pliku wykonywalnym lub w osobnym pliku symboli [5].

GDB obsługuje symbole w formacie STABS/STAB oraz DWARF, potrafi również odczytać tablicę symboli w plikach ELF oraz COFF, XCOFF, ECOFF [7]. W przeciwieństwie do formatu ELF, tablica symboli COFF jest dużo bardziej szczegółowa [8,9] i może zawierać więcej elementów przydatnych podczas odpluskwiania.

Bardzo często, by dołączyć odpowiednie symbole debugowania, wystarczy użyć przełącznika `-g` podawanego kompilatorowi. Tak jest między innymi w GCC [10], clang [11] oraz we Free Pascal [12]. Niektóre kompilatory pozwalają umieścić symbole debugowania w osobnym pliku (np. Free Pascal [12]), w innym przypadku należy samodzielnie wygenerować taki plik poprzez wyodrębnienie symboli odpluskwiania z pliku całościowego. Poniżej zaprezentowano przykład takiej operacji z użyciem narzędzia `objcopy` [13]::

  $ g++ -g example.cpp -o example.out
  $ objcopy --only-keep-debug example.out example.debug
  $ strip -g example.out
  $ objcopy --add-gnu-debuglink=example.debug example.out

W pierwszej linii powyższego wydruku wykonujemy kompilację z użyciem przełącznika `-g`, co spowoduje utworzenie pliku wykonywalnego wraz z dodatkowymi symbolami. W drugiej linii dodatkowe symbole są kopiowane do osobnego pliku, a w trzeciej usuwane z pliku całościowego. Ostatnim krokiem jest umieszczenie informacji o dodatkowym pliku z symbolami w pliku wykonywalnym – ta informacja zostanie wykorzystana przez GDB do znalezienia dodatkowych symboli.


Uruchomienie aplikacji pod nadzorem GDB
---------------------------------------

Uruchomienie aplikacji z odpluskwiaczem sprowadza się do wykonania odpowiedniego polecenia w konsoli::

  $ gdb ./example.out
  Reading symbols from ./example.out...done.
  (gdb) run

W pierwszej linii widzimy polecenie uruchamiające `gdb` ze ścieżką do interesującego nas pliku wykonywalnego. Po jego wykonaniu symbole zostaną załadowane automatycznie. Druga linia — polecenie `run` w interaktywnym trybie debuggera — odpowiada za uruchomienie wskazanej aplikacji.

Polecenie run może także przyjmować argumenty, które zostaną przekazane do programu. W poniższym przykładzie zaprezentowano przekazanie trzech parametrów – 'arg1', 3 oraz 2::

  $ gdb ./example.out
  Reading symbols from ./example.out...done.
  (gdb) run 'arg1' 3 2

GDB możemy również uruchomić bez argumentów, a plik wykonywalny zdefiniować w trybie interaktywnym za pomocą polecenia `file`::

  $ gdb
  (gdb) file ./example.out
  Reading symbols from ./example.out...done.
  (gdb) run

Gdyby automatyczne załadowanie symboli nie powiodło się, możemy ręcznie podać ścieżkę do pliku, z którego mają zostać załadowane. Służy do tego polecenie `symbol-file` w trybie interaktywnym::

  $ gdb
  (gdb) file example.out
  Reading symbols from example.out...(no debugging symbols found)...done.
  (gdb) symbol-file example.debug
  Reading symbols from example.debug...done.
  (gdb) run

Do analizy programu możemy wykorzystać plik zrzutu pamięci (zachęcam do zapoznania się z `artykułem na temat core dump </blog/Linux_-_Core_dump/>`__). Informację na jego temat przekazujemy podczas uruchamiania GDB::

  $ gdb ./example.out example.core-dump

W trybie interaktywnym służy do tego polecenie `core-file`::

  $ gdb ./example.out
  (gdb) core-file example.core-dump

GDB może zostać użyty do analizy działającego procesu. Identyfikator interesującego nas procesu (PID) podajemy w linii poleceń. Przykład dla procesu o numerze *1593*::

  $ gdb ./example.out 1593

Podłączenie do procesu może się także odbyć w trybie interaktywnym za pomocą polecenia `attach`::

  $ gdb ./example.out
  (gdb) attach 1593

Zamknięcie GDB następuje po wykonaniu polecenia `quit`::

  $ gdb ./example.out
  (gdb) quit

Wszystkie omówione opcje zostały przedstawione w oficjalnej dokumentacji [14,15,16].


Debugowanie aplikacji
---------------------

Poniżej przedstawiam kilka, moim zdaniem, najważniejszych poleceń przydatnych podczas analizy. Przykładową aplikację treningową możesz znaleźć `w repozytorium GitHub <https://github.com/chyla/GdbTutorial>`__.


Pułapki
^^^^^^^

Pułapki (ang. breakpoint) wskazują miejsce, w którym działanie programu zostanie wstrzymane. Do ich ustawienia służy polecenie `break`, które jako argument przyjmuje lokalizację – nazwę funkcji, względny/bezwzględny numer linii lub adres instrukcji [17].

Poniżej przykład ustawienia pułapki z użyciem nazwy funkcji::

  $ gdb break.out
  (gdb) break test_break 
  Breakpoint 1 at 0x40077a: file break.cpp, line 7.
  (gdb) run
  Starting program: /vagrant/break.out
  
  Breakpoint 1, test_break () at break.cpp:7
  7               cout << "Test break\n";
  (gdb) 


Przykład ustawienia pułapki z użyciem nazwy pliku i numeru linii::

  $ gdb break.out
  (gdb) break break.cpp:6
  Breakpoint 1 at 0x40077a: file break.cpp, line 6.
  (gdb) run
  Starting program: /vagrant/break.out
 
  Breakpoint 1, test_break () at break.cpp:7
  7               cout << "Test break\n";


Listę aktualnie ustawionych pułapek możemy sprawdzić poleceniem `info breakpoints` lub krócej `info break` [17]::

  (gdb) info break 
  Num     Type           Disp Enb Address            What
  1       breakpoint     keep y   0x000000000040077a in test_break() at break.cpp:7


Punkty obserwacji
^^^^^^^^^^^^^^^^^

Punkt obserwacji (ang. watchpoint) pozwala zatrzymać wykonywanie programu, gdy wartość wyrażenia przekazanego jako argument polecenia `watch` ulegnie zmianie. Wyrażeniem może proste (np. złożone z nazwy zmiennej) lub złożone (np. rzutowanie wartości pod określonym adresem na dany typ danych, wrażenie matematyczne) [18].

Przykład obserwacji zmiennej w strukturze::

  $ gdb watch.out  
  (gdb) break main 
  Breakpoint 1 at 0x4006df: file watch.cpp, line 21. 
  (gdb) run 
  Starting program: /vagrant/watch.out  
  
  Breakpoint 1, main (argc=1, argv=0x7fffffffe5d8) at watch.cpp:21 
  21              tsw.y = 0; 
  (gdb) watch tsw.y 
  Hardware watchpoint 2: tsw.y 
  (gdb) continue 
  Continuing. 
  
  Hardware watchpoint 2: tsw.y 
  
  Old value = -6704 
  New value = 0 
  main (argc=1, argv=0x7fffffffe5d8) at watch.cpp:22 
  22              tsw.y++;


Przykład obserwacji wyrażenia::

  $ gdb watch.out
  (gdb) break test_watch 
  Breakpoint 1 at 0x4006ba: file watch.cpp, line 11. 
  (gdb) run 
  Starting program: /vagrant/watch.out  
  
  Breakpoint 1, test_watch () at watch.cpp:11 
  11              int x = 0; 
  (gdb) watch x < 2 
  Hardware watchpoint 2: x < 2 
  (gdb) continue 
  Continuing. 
  
  Hardware watchpoint 2: x < 2 
  
  Old value = true 
  New value = false 
  test_watch () at watch.cpp:12 
  12              while (x < 10) {


Listę ustawionych pułapek i punktów obserwacji można sprawdzić poleceniem `info break` oraz `info watchpoints`::

  $ gdb watch.out  
 (gdb) break main 
 Breakpoint 1 at 0x4006df: file watch.cpp, line 21. 
 (gdb) run 
 Starting program: /vagrant/watch.out  
 
 Breakpoint 1, main (argc=1, argv=0x7fffffffe5d8) at watch.cpp:21 
 21              tsw.y = 0; 
 (gdb) watch tsw.y 
 Hardware watchpoint 2: tsw.y 
 (gdb) info break 
 Num     Type           Disp Enb Address            What 
 1       breakpoint     keep y   0x00000000004006df in main(int, char**) at watch.cpp:21 
        breakpoint already hit 1 time 
 2       hw watchpoint  keep y                      tsw.y 
 (gdb) info watchpoints  
 Num     Type           Disp Enb Address            What 
 2       hw watchpoint  keep y                      tsw.y


Usuwanie pułapek i punktów obserwacji
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Do usuwania ustawionych pułapek i punktów obserwacji służą polecenia: `clear` oraz `delete`. `clear` bazuje na ich położeniu (np. nazwie funkcji, numerze linii), natomiast `delete` bazuje na przydzielonym im numerze identyfikacyjnym [19]. Numer ten jest wyświetlany podczas tworzenia pułapki oraz punktu obserwacji, można go także ustalić poleceniem `info break`.

Przykład usunięcia pułapki bazując na jej numerze::

  $ gdb break.out 
  (gdb) break main 
  Breakpoint 1 at 0x40079b: file break.cpp, line 12. 
  (gdb) break test_break 
  Breakpoint 2 at 0x40077a: file break.cpp, line 7. 
  (gdb) info break 
  Num     Type           Disp Enb Address            What 
  1       breakpoint     keep y   0x000000000040079b in main(int, char**) at break.cpp:12 
  2       breakpoint     keep y   0x000000000040077a in test_break() at break.cpp:7 
  (gdb) delete 1 
  (gdb) info break 
  Num     Type           Disp Enb Address            What 
  2       breakpoint     keep y   0x000000000040077a in test_break() at break.cpp:7


Przykład usunięcia pułapki bazując na jej położeniu::

  $ gdb watch.out  
  (gdb) break main 
  Breakpoint 1 at 0x4006df: file watch.cpp, line 21. 
  (gdb) break test_watch 
  Breakpoint 2 at 0x4006ba: file watch.cpp, line 11. 
  (gdb) info break 
  Num     Type           Disp Enb Address            What 
  1       breakpoint     keep y   0x00000000004006df in main(int, char**) at watch.cpp:21 
  2       breakpoint     keep y   0x00000000004006ba in test_watch() at watch.cpp:11 
  (gdb) clear watch.cpp:21 
  Deleted breakpoint 1 
  (gdb) clear test_watch 
  Deleted breakpoint 2 


Polecenia nawigacji
^^^^^^^^^^^^^^^^^^^

Polecenia nawigacji po analizowanej aplikacji można podzielić na dwie kategorie: pierwszą związaną z poruszaniem się po kodzie/instrukcjach programu oraz drugą związaną z poruszaniem się po poszczególnych ramkach stosu programu (`zachęcam do zapoznania się z moim artykułem na temat stosu </blog/assembler/Asembler_cz2_Stos_i_wywolanie_funkcji/>`__).

Do **nawigacji po kodzie/instrukcjach** służą polecenia:

* `list`
* `next`
* `step`
* `finish`
* `continue`

Polecenie `list` [24] pozwala przeglądać kod źródłowy programu. Argumentem może być numer linii w pliku, zakres linii, czy nazwa funkcji. Domyślnie wyświetlane jest tylko 10 linii, by to zmienić należy wykorzystać polecenie `set listsize`.

Poniższy przykład prezentuje wyświetlenie aktualnej wartości oraz zmianę domyślnie wyświetlanej liczby linii kodu źródłowego, a także wyświetlenie kodu źródłowego przykładowej funkcji `main`::

  $ gdb navigation.out
  (gdb) show listsize
  Number of source lines gdb will list by default is 10.
  (gdb) set listsize 5
  (gdb) show listsize
  Number of source lines gdb will list by default is 5.
  (gdb) list main
  11	}
  12	
  13	int main(int argc, char **argv) {
  14		int val = 0;
  15	


Zauważmy, że funkcja `main` została umieszczona pośrodku. Do wyświetlenia funkcji od jej początku można posłużyć się zakresem (początek wskazuje na funkcję `main`, a koniec jest nieokreślony – przecinek pełni istotną rolę)::

  $ gdb navigation.out 
  (gdb) set listsize 5
  (gdb) list main,
  13	int main(int argc, char **argv) {
  14		int val = 0;
  15	
  16		increment(val);
  17	


`next`, `step`, `finish` oraz `continue` pozwalają sterować przebiegiem wykonania programu [25]. `next` wykonuje instrukcje odpowiadające kolejnej linii kodu źródłowego, jeśli jest to funkcja to zostanie ona wykonana. `step` również wykonuje kolejną linię kodu, jednak jeśli jest to funkcja to przechodzi do niej. `finish` wykonuje kolejne instrukcje, aż do zakończenia obecnej funkcji.  `continue` wznawia pracę programu.

Przykład wykorzystania powyższych poleceń::

  $ gdb navigation.out
  (gdb) break main
  Breakpoint 1 at 0x400769: file navigation.cpp, line 13.
  (gdb) run
  Starting program: /vagrant/navigation.out 
  
  Breakpoint 1, main (argc=1, argv=0x7fffffffe5d8) at navigation.cpp:13
  13	int main(int argc, char **argv) {
  (gdb) next
  14		int val = 0;
  (gdb) next
  16		increment(val);
  (gdb) next
  18		decrement(val);
  (gdb) step
  decrement (x=@0x7fffffffe4e4: 1) at navigation.cpp:10
  10		x--;
  (gdb) finish
  Run till exit from #0  decrement (x=@0x7fffffffe4e4: 1) at navigation.cpp:10
  main (argc=1, argv=0x7fffffffe5d8) at navigation.cpp:20
  20		val += 10;
  Value returned is $1 = -6940
  (gdb) continue
  Continuing.
  [Inferior 1 (process 6775) exited normally]


Do **nawigacji po ramkach stosu** służą polecenia:

* `backtrace` (inaczej `bt`, `where` lub `info stack`)
* `frame`
* `up`
* `down`

`backtrace` [26] wyświetla podsumowanie o wywołanych funkcjach. Na jedną linię podsumowania przypada jedna ramka stosu, w każdej linii zawarta jest informacja o numerze wykonanej linii w pliku źródłowym.

Na poniższym wydruku widzimy, że program wykonał funkcję `main` aż do linii 18, w której to zaczął wykonywać funkcję `decrement` aż do linii 10::

  $ gdb navigation.out 
  (gdb) break decrement
  Breakpoint 1 at 0x400748: file navigation.cpp, line 10.
  (gdb) run
  Starting program: /vagrant/navigation.out 
  
  Breakpoint 1, decrement (x=@0x7fffffffe4e4: 1) at navigation.cpp:10
  10		x--;
  (gdb) where
  #0  decrement (x=@0x7fffffffe4e4: 1) at navigation.cpp:10
  #1  0x0000000000400797 in main (argc=1, argv=0x7fffffffe5d8) at navigation.cpp:18

`frame` wyświetla informacje o aktualnie wybranej ramce stosu, natomiast polecenia `up` oraz `down` pozwalają ją zmienić [27]. Po wybraniu ramki stosu możemy wykonywać na niej inne operacje – np. wyświetlanie wartości zmiennych dostępnych w wybranej ramce.

Poniżej przykład prezentujący wybrane polecenia::

  $ gdb navigation.out 
  (gdb) break decrement
  Breakpoint 1 at 0x400748: file navigation.cpp, line 10.
  (gdb) run
  Starting program: /vagrant/navigation.out 
  
  Breakpoint 1, decrement (x=@0x7fffffffe4e4: 1) at navigation.cpp:10
  10		x--;
  (gdb) where
  #0  decrement (x=@0x7fffffffe4e4: 1) at navigation.cpp:10
  #1  0x0000000000400797 in main (argc=1, argv=0x7fffffffe5d8) at navigation.cpp:18
  (gdb) frame
  #0  decrement (x=@0x7fffffffe4e4: 1) at navigation.cpp:10
  10		x--;
  (gdb) up
  #1  0x0000000000400797 in main (argc=1, argv=0x7fffffffe5d8) at navigation.cpp:18
  18		decrement(val);
  (gdb) frame
  #1  0x0000000000400797 in main (argc=1, argv=0x7fffffffe5d8) at navigation.cpp:18
  18		decrement(val);
  (gdb) down
  #0  decrement (x=@0x7fffffffe4e4: 1) at navigation.cpp:10
  10		x--;
  (gdb) frame
  #0  decrement (x=@0x7fffffffe4e4: 1) at navigation.cpp:10
  10		x--;


Ustawienie oraz wyświetlenie zmiennych
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Do ustawiania oraz wyświetlania zmiennych (de facto wyrażeń) możemy użyć poleceń `set`, `print`, `display` oraz `undisplay`. 

`set` pozwala ustawić wartość zmiennej [28]. Jeśli nazwa zmiennej koliduje z nazwą jednego z podpolecenia `set`, to możemy użyć `set variable`.

Poniżej przykład wykorzystania polecenia `set` oraz `set variable`::

  $ gdb loop.out 
  (gdb) break test_loop
  Breakpoint 1 at 0x40072a: file loop.cpp, line 7.
  (gdb) run
  Starting program: /vagrant/loop.out 
  
  Breakpoint 1, test_loop () at loop.cpp:7
  7		int b = 2;
  (gdb) next
  8		int i = 0;
  (gdb) next
  10		while (i == 0) {
  (gdb) set i=1
  Ambiguous set command "i=1": .
  (gdb) set variable i=1
  (gdb) set variable i=b+1


Kolejną instrukcją jest `print`. Jest ona o tyle ciekawa, że oprócz wypisywania wartości zmiennej pozwala ją także ustawić [28]. 

Poniżej przykład wykorzystania polecenia `print`::

  $ gdb loop.out 
  (gdb) break test_loop
  Breakpoint 1 at 0x40072a: file loop.cpp, line 7.
  (gdb) run
  Starting program: /vagrant/loop.out 
  
  Breakpoint 1, test_loop () at loop.cpp:7
  7		int b = 2;
  (gdb) next
  8		int i = 0;
  (gdb) next
  10		while (i == 0) {
  (gdb) print b
  $1 = 2
  (gdb) print i
  $2 = 0
  (gdb) print i=1+2*b
  $3 = 5
  (gdb) print i
  $4 = 5


Warto wiedzieć, że polecenie `print` może wyświetlać dane w różnym formacie. Jego specyfikację podaje się jako pierwszy argument - `print /FORMAT expression`.

Możliwe formaty wyświetlania danych [30, 31]:

* o - octal
* x - hexadecimal
* u - unsigned decimal
* t - binary
* f - floating point
* a - address
* c - char
* s - string

Przykład formatowania danych::

  (gdb) print /c 65
  $9 = 65 'A'
  (gdb) print /x 65
  $10 = 0x41


Polecenie `display` jest w swoim działaniu bardzo podobne do `print`, jednakże `display` wyświetla podane wyrażenie przy każdym zatrzymaniu programu. `list display` informuje o aktualnych wyrażeniach, a `undisplay` (lub `delete display`) pozwala je usunąć. `display` umożliwia także wyspecyfikowanie formatu wyświetlanych danych — w dokładnie ten sam sposób jak przy poleceniu `print`.

Przykład wykorzystania omówionych poleceń::

  $ gdb watch.out 
  (gdb) break test_watch
  Breakpoint 1 at 0x4006ba: file watch.cpp, line 11.
  (gdb) run
 Starting program: /vagrant/watch.out 
  
  Breakpoint 1, test_watch () at watch.cpp:11
  11		int x = 0;
  (gdb) next
  12		while (x < 10) {
  (gdb) display x
  1: x = 0
  (gdb) display x < 10
  2: x < 10 = true
  (gdb) next
  13			x++;
  1: x = 0
  2: x < 10 = true
  (gdb) next
  12		while (x < 10) {
  1: x = 1
  2: x < 10 = true
  (gdb) next
  13			x++;
  1: x = 1
  2: x < 10 = true
  (gdb) next
  12		while (x < 10) {
  1: x = 2
  2: x < 10 = true
  (gdb) info display
  Auto-display expressions now in effect:
  Num Enb Expression
  1:   y  x
  2:   y  x < 10
  (gdb) undisplay 1
  (gdb) next
  13			x++;
  2: x < 10 = true
  (gdb) display /x x
  3: /x x = 0x2
  (gdb) next
  12		while (x < 10) {
  2: x < 10 = true
  3: /x x = 0x3


Warto również wiedzieć o poleceniach `info args` oraz `info locals` [32]. Polecenia te wyświetlają odpowiednio wartości argumentów oraz zmiennych lokalnych.


Obsługa wielowątkowości
^^^^^^^^^^^^^^^^^^^^^^^

GDB pozwala również analizować programy wielowątkowe [33]. Utworzone wątki są wykrywane automatycznie, co obrazuje poniższy przykład::

  $ gdb threads.out
  (gdb) break my_thread
  Breakpoint 1 at 0x400e90: file threads.cpp, line 8.
  (gdb) run
  Starting program: /vagrant/threads.out 
  [Thread debugging using libthread_db enabled]
  Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
  [New Thread 0x7ffff6f4e700 (LWP 7856)]
  [New Thread 0x7ffff674d700 (LWP 7857)]
  [Switching to Thread 0x7ffff6f4e700 (LWP 7856)]
  
  Thread 2 "threads.out" hit Breakpoint 1, my_thread () at threads.cpp:8
  8		for (int i = 0; i < 10; i++) {


Moim zdaniem najbardziej przydatnymi poleceniami do pracy na wątkach są `info threads` oraz `thread`. `info threads` wyświetla informacje dotyczące wątków (np. identyfikator, aktualna ramka stosu), `thread` wybiera wątek, na którym będziemy pracować.

Poniżej przykład pracy na dwóch wątkach – po wybraniu wątku praca odbywa się jak dotychczas::

  $ gdb threads.out 
  (gdb) break my_thread
  Breakpoint 1 at 0x400fb0: file threads.cpp, line 8.
  (gdb) run
  Starting program: /vagrant/threads.out 
  [Thread debugging using libthread_db enabled]
  Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
  [New Thread 0x7ffff6f4e700 (LWP 7996)]
  [New Thread 0x7ffff674d700 (LWP 7997)]
  [Switching to Thread 0x7ffff6f4e700 (LWP 7996)]
  
  Thread 2 "threads.out" hit Breakpoint 1, my_thread () at threads.cpp:8
  8		for (int i = 0; i < 10; i++) {
  (gdb) step
  [Switching to Thread 0x7ffff674d700 (LWP 7997)]
  
  Thread 3 "threads.out" hit Breakpoint 1, my_thread () at threads.cpp:8
  8		for (int i = 0; i < 10; i++) {
  (gdb) thread 2
  [Switching to thread 2 (Thread 0x7ffff6f4e700 (LWP 7996))]
  #0  0x0000000000400fb7 in my_thread () at threads.cpp:8
  8		for (int i = 0; i < 10; i++) {
  (gdb) step
  Value: 0
  Value: 1
  Value: 2
  Value: 3
  Value: 4
  Value: 5
  Value: 6
  Value: 7
  Value: 8
  Value: 9
  [Thread 0x7ffff674d700 (LWP 7997) exited]
  9			cout << "Value: " << i << endl;
  (gdb) step
  Value: 0
  8		for (int i = 0; i < 10; i++) {
  (gdb) step
  9			cout << "Value: " << i << endl;


Warto zauważyć, że **GDB podczas pracy skupia się tylko na jednym wątku**. W przykładzie powyżej zaprezentowano, jak po wykonaniu polecenia `step`, wątek 3 (nieustawiony) kontynuuje pracę – tylko wątek 2 jest pod kontrolą odpluskwiacza.

Podczas napotkania jakiejkolwiek pułapki wstrzymywane są wszystkie wątki, natomiast po wznowieniu pracy każdy wątek rozpocznie działanie, jednak tylko jeden będzie pod obserwacją GDB.


Tekstowy interfejs użytkownika
------------------------------

Oprócz znanego wszystkim interaktywnego interfejsu GDB posiada także specjalny tekstowy interfejs użytkownika (Text User Inteface – TUI) [34]. Za jego aktywację odpowiada polecenie `tui enable`, natomiast za dezaktywację `tui disable` - można także użyć skrótu klawiszowego *CTRL-x a*.

.. figure:: /images/artykuly/cpp/gdb-tutorial-tui.png

   Przykładowa sesja TUI z widokiem src.


Dostępnych jest kilka układów okien (standardowym jest `src`) możliwych do przełączenia za pomocą polecenia `layout <nazwa>`.

* `src` – okno kodu źródłowego oraz wiersz poleceń
* `asm` – okno assemblera oraz wiersz poleceń
* `split` – okno kodu źródłowego, assemblera i wiersza poleceń
* `regs` – jeśli w momencie przełączenia aktualnym układem był `src` to ustawione zostanie okno rejestrów, kodu źródłowego i wiersza poleceń; jeśli układem był `asm` lub `split` to ustawione zostanie okno rejestrów, assemblera i wiersza poleceń.

.. figure:: /images/artykuly/cpp/gdb-tutorial-tui-split.png

   Przykładowa sesja TUI z widokiem split.


Aktualnie aktywne okno można przełączyć za pomocą skrótu klawiszowego *CTRL-x o*.

Ten rodzaj interfejsu użytkownika posiada specjalny tryb (TUI Single Key Mode), w którym najczęściej używane polecenia otrzymały swój jedno-znakowy skrót klawiszowy, aby przełączyć się do tego trybu należy użyć skrótu *CTRL-x s*.

Niektóre skróty klawiszowe:

* c - continue
* d - down
* f - finish
* n - next
* q – wyjdź z trybu
* r - run
* s - step
* u - up
* w - where

GDB to potężne narzędzie. Warto poznać podstawy jego obsługi, by w przyszłości móc z łatwością wykorzystać jego potencjał w praktyce.


Literatura
----------

1. `GDB: The GNU Project Debugger <https://www.gnu.org/software/gdb/>`__
2. `Debugging with GDB: Supported Languages <http://sourceware.org/gdb/current/onlinedocs/gdb/Supported-Languages.html#Supported-Languages>`__
3. `GDB 8.0 Released, Adds Many New Features, Drops Java GCJ Support - Phoronix <https://www.phoronix.com/scan.php?page=news_item&px=GNU-GDB-8.0-Released>`__
4. `GCC 7 Release Series; Changes, New Features, and Fixes - GNU Project - Free Software Foundation (FSF) <https://gcc.gnu.org/gcc-7/changes.html>`__
5. `Symbols and Symbol Files <https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/symbols-and-symbol-files>`__
6. `Debugging formats DWARF and STAB <https://www.ibm.com/developerworks/library/os-debugging/>`__
7. `Opcje odpluskwiania w gcc. Formaty plików obiektowych i przygotowanych do odpluskwiania. <http://students.mimuw.edu.pl/SO/Projekt05-06/temat3-g3/pliki_obiektowe.html>`__
8. `Inside ELF Symbol Tables | Oracle Ali Bahrami Blog <https://blogs.oracle.com/ali/inside-elf-symbol-tables>`__
9. `COFF: Symbol Table <http://www.delorie.com/djgpp/doc/coff/symtab.html>`__
10. `Using the GNU Compiler Collection (GCC): Debugging Options <https://gcc.gnu.org/onlinedocs/gcc/Debugging-Options.html>`__
11. `clang - the Clang C, C++, and Objective-C compiler - Clang 6 documentation <https://clang.llvm.org/docs/CommandGuide/clang.html>`__
12. `Logging exceptions - Free Pascal wiki <http://wiki.freepascal.org/Logging_exceptions>`__
13. `Debugging with GDB: Separate Debug Files <https://sourceware.org/gdb/onlinedocs/gdb/Separate-Debug-Files.html>`__
14. `Debugging with GDB: Invoking GDB <https://sourceware.org/gdb/current/onlinedocs/gdb/Invoking-GDB.html#Invoking-GDB>`__
15. `Debugging with GDB: Files <https://sourceware.org/gdb/current/onlinedocs/gdb/Files.html#Files>`__
16. `Debugging with GDB: Attach <https://sourceware.org/gdb/onlinedocs/gdb/Attach.html>`__
17. `Debugging with GDB: Set Breaks <https://sourceware.org/gdb/onlinedocs/gdb/Set-Breaks.html>`__
18. `Debugging with GDB: Set Watchpoints <https://sourceware.org/gdb/onlinedocs/gdb/Set-Watchpoints.html>`__
19. `Debugging with GDB: Delete Breaks <https://sourceware.org/gdb/onlinedocs/gdb/Delete-Breaks.html#Delete-Breaks>`__
20. `Debugging with GDB: List <https://sourceware.org/gdb/onlinedocs/gdb/List.html>`__
21. `Debugging with GDB: Continuing and Stepping <https://sourceware.org/gdb/onlinedocs/gdb/Continuing-and-Stepping.html>`__
22. `Debugging with GDB: Backtrace <https://sourceware.org/gdb/onlinedocs/gdb/Backtrace.html>`__
23. `Debugging with GDB: Selection <https://sourceware.org/gdb/onlinedocs/gdb/Selection.html>`__
24. `Debugging with GDB: List <https://sourceware.org/gdb/onlinedocs/gdb/List.html>`__
25. `Debugging with GDB: Continuing and Stepping <https://sourceware.org/gdb/onlinedocs/gdb/Continuing-and-Stepping.html>`__
26. `Debugging with GDB: Backtrace <https://sourceware.org/gdb/onlinedocs/gdb/Backtrace.html>`__
27. `Debugging with GDB: Selection <https://sourceware.org/gdb/onlinedocs/gdb/Selection.html>`__
28. `Debugging with GDB: Assignment to Variables <https://www.sourceware.org/gdb/onlinedocs/gdb.html#Assignment>`__
29. `Debugging with GDB: Automatic Display <https://sourceware.org/gdb/onlinedocs/gdb/Auto-Display.html>`__
30. `Debugging with GDB: Output Formats <https://sourceware.org/gdb/onlinedocs/gdb/Output-Formats.html#Output-Formats>`__
31. `GDB Command Reference - print command <http://visualgdb.com/gdbreference/commands/print>`__
32. `Debugging with GDB: Frame Info <https://sourceware.org/gdb/onlinedocs/gdb/Frame-Info.html>`__
33. `Debugging with GDB: Threads <https://sourceware.org/gdb/onlinedocs/gdb/Threads.html>`__
34. `GDB Text User Interface <https://sourceware.org/gdb/current/onlinedocs/gdb/TUI.html#TUI>`__

