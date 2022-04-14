Core dump
=========

Core dump to plik zawierający zapis stanu programu z chwili, w której wystąpiło żądanie jego utworzenia. Mogło ono zostać spowodowane awarią aplikacji lub działaniem użytkownika.


Automatyczne generowanie pliku core
-----------------------------------

Plik core (zrzut pamięci) zostanie automatycznie wygenerowany przez jądro systemu, gdy aplikacja ulegnie awarii *(crash)* i nie jest w stanie kontynuować swojej pracy. Może tak się stać na przykład, gdy nastąpi próba zapisu do niezaalokowanej pamięci lub wykonania błędnej instrukcji procesora...

Muszą zostać spełnione odpowiednie warunki, aby było możliwe wykonanie zrzutu. Elementem, na który trzeba zwrócić uwagę, jest limit rozmiaru pliku core. Sprawdzić go możemy za pomocą polecenia ``ulimit``::

  $ ulimit -a
  core file size          (blocks, -c) 0
  data seg size           (kbytes, -d) unlimited
  scheduling priority             (-e) 0
  file size               (blocks, -f) unlimited
  pending signals                 (-i) 29175
  max locked memory       (kbytes, -l) 64
  max memory size         (kbytes, -m) unlimited
  open files                      (-n) 1024
  pipe size            (512 bytes, -p) 8
  POSIX message queues     (bytes, -q) 819200
  real-time priority              (-r) 0
  stack size              (kbytes, -s) 8192
  cpu time               (seconds, -t) unlimited
  max user processes              (-u) 29175
  virtual memory          (kbytes, -v) unlimited
  file locks                      (-x) unlimited

  $ ulimit -c
  0

``ulimit -a`` wypisze wszystkie ustawione limity, natomiast ``ulimit -c`` wypisze tylko limit maksymalnego rozmiaru pliku core.

Na powyższym przykładzie widzimy, że maksymalny rozmiar pliku wynosi zero. W takim przypadku nie zostanie on utworzony. Możemy określić dokładny rozmiar lub przypisać wartość *unlimited*, co pozwoli na tworzenie dowolnie dużych plików zrzutu::

  $ ulimit -c unlimited

  $ ulimit -c
  unlimited

Powyższe ustawienie zadziała tylko dla aktualnej sesji (np. aktualnie otwartej sesji bash, aktualnie otwartego okna terminala), aby było ono stosowane dla każdej nowej sesji każdego użytkownika, musimy dodać do pliku ``/etc/security/limits.conf`` linię::

  *               soft    core            unlimited

Jeżeli nie chcemy modyfikować pliku ``limits.conf``, to istnieje możliwość utworzenia nowego pliku konfiguracyjnego w ``/etc/security/limits.d/`` z dokładnie tą samą linią jak powyżej.

O pozostałych warunkach, które trzeba spełnić, by został wygenerowany plik core, przeczytasz w ``man 5 core``. Nie wspominam o nich, gdyż to właśnie limity są najczęściej zmieniane. W manualu znajdziesz również informacje o możliwych przyczynach, które spowodują jego wygenerowanie.


Samodzielne wygenerowanie pliku core
------------------------------------

Plik zrzutu możemy również wygenerować samodzielnie za pomocą polecenia ``gcore``. Nie wymaga to przerywania pracy programu - proces ten będzie działał poprawnie również po wykonaniu zrzutu.

Oto przebieg przykładowej sesji, w której wygenerowano plik core dla aktualnie uruchomionego shella Bash::

  $ ps
  PID TTY          TIME CMD
  15665 pts/7    00:00:00 bash
  15689 pts/7    00:00:00 ps

  $ gcore -o moj_plik_zrzutu 15665
  0x00007f4ba32bd58a in __GI___waitpid (pid=-1, stat_loc=0x7ffed73b4280, options=10) at ../sysdeps/unix/sysv/linux/waitpid.c:29
  29        return SYSCALL_CANCEL (wait4, pid, stat_loc, options, NULL);
  Saved corefile moj_plik_zrzutu.15665

  $ ls -lh moj_plik_zrzutu.15665
  -rw-rw-r--. 1 adam adam 1,4M 04-11 14:44 moj_plik_zrzutu.15665

Polecenie ``gcore`` działa niezależnie od ustawienia limitu rozmiaru pliku core. Opcja ``-o`` pozwala na zdefiniowanie własnej nazwy, do której dołączony zostaje numer PID. Drugim argumentem do programu jest numer procesu, dla którego tworzymy plik core.

Wygenerowanie pliku core możemy również wymusić poprzez wysłanie sygnału do procesu, np. *abort*::

  $ kill -ABRT 15665
  Aborted (zrzut pamięci)

  $ ls

W takim przypadku zrzut został wykonany przez jądro systemu operacyjnego. Argument ``-ABRT`` identyfikuje sygnał, który chcemy wysłać. Liczba *15665* to oczywiście numer procesu.


Nazwa pliku core
----------------

Nazwa pliku core powstaje według określonego formatu przechowywanego w parametrze jądra ``kernel.core_pattern``. Za jego pomocą możemy zmienić nazwę generowanego pliku core oraz miejsce, w którym zostanie zapisany. Zobaczmy::

  $ sysctl kernel.core_pattern=/tmp/core-%h.%p

  $ sleep 90 &
  [1] 22237

  $ ps
  PID TTY          TIME CMD
  21845 pts/7    00:00:00 bash
  22237 pts/7    00:00:00 sleep
  22240 pts/7    00:00:00 ps

  $ kill -ABRT 22237
  [1]+  Aborted                 (zrzut pamięci) sleep 90

  $ ls -al /tmp/core-Dahlia.22237
  -rw-------. 1 adam adam 393216 04-11 18:34 /tmp/core-Dahlia.22237

Jądro umieściło plik core w katalogu */tmp* pod nazwą *core-Dahlia.22237*. Specyfikatory ``%h`` oraz ``%p`` ze wzorca zostały zamienione przez nazwę hosta oraz PID procesu. Oto lista niektórych specyfikatorów (więcej znajdziesz w ``man 5 core``):

* ``%e`` - nazwa pliku wykonywalnego
* ``%g`` - numer identyfikacyjny grupy, na prawach której był uruchomiony proces
* ``%h`` - nazwa hosta
* ``%p`` lub ``%P`` - numer procesu
* ``%s`` - numer sygnału, który spowodował zrzut pamięci
* ``%t`` - czas w jakim powstał plik zrzutu
* ``%u`` - numer identyfikacyjny użytkownika, na prawach którego był uruchomiony proces

Wzorzec może rozpoczynać się od znaku `|` (pipe). Oznacza to, że zostanie wywołany program, którego ścieżkę podano po znaku pipe, a na jego standardowe wejście zostanie przekazany zrzut pamięci. Podjęte działanie zależy wtedy od wywołanego programu, może to być zapis zrzutu pamięci do pliku core lub inne działanie (np. wysłanie zgłoszenia błędu do autora danego programu).

Oto przykład, w którym na standardowe wejście programu ``systemd-coredump`` zostanie przekazany zrzut pamięci::

  $ sysctl kernel.core_pattern
  kernel.core_pattern = |/usr/lib/systemd/systemd-coredump %P %u %g %s %t %c %e


GNU Debugger (GDB)
------------------

Plik core wykorzystywany jest podczas analizy z użyciem programu ``gdb``. W tym celu jako argument należy podać ścieżkę do pliku binarnego aplikacji oraz ścieżkę do pliku core::

  $ gdb /bin/sleep sleep.core
    // ... //
  Core was generated by `sleep'.
  Program terminated with signal 6, Aborted.
  Reading symbols from /lib/libc.so.7...(no debugging symbols found)...done.
  Loaded symbols for /lib/libc.so.7
  Reading symbols from /libexec/ld-elf.so.1...(no debugging symbols found)...done.
  Loaded symbols for /libexec/ld-elf.so.1
  #0  0x00000008008fa95a in _nanosleep () from /lib/libc.so.7
  (gdb) where
  #0  0x00000008008fa95a in _nanosleep () from /lib/libc.so.7
  #1  0x00000000004009e6 in ?? ()
  #2  0x000000000040086f in ?? ()
  #3  0x0000000800621000 in ?? ()
  #4  0x0000000000000000 in ?? ()
  (gdb)

Polecenie ``where`` pokazuje kolejne ramki stosu procesu.


Literatura
------------

1. `core(5) <https://linux.die.net/man/5/core>`__
2. `How to generate a core dump in Linux when a process gets a segmentation fault? <https://stackoverflow.com/questions/17965/how-to-generate-a-core-dump-in-linux-when-a-process-gets-a-segmentation-fault>`__
