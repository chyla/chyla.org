GDB - Breakpoint na funkcji w anonimowej przestrzeni nazw C++
=============================================================

Wykorzystując instrukcję ``break`` możemy ustawić pułapkę na daną funkcję. Na ogół nie sprawia trudności ustawienie jej na funkcję globalną, metodę klasy, czy funkcję w nazwanej przestrzeni nazw (za pomocą ``::``).

.. code:: cpp

  #include <iostream>

  using namespace std;

  namespace {

  int funkcja() {
      return 5;
  } 

  }

  int main(int argc, char *argv[]) {
      cout << funkcja() << '\n';

      return 0;
  }


W przypadku anonimowej przestrzeni nazw przed ``::`` zamiast nazwy przestrzeni, czy klasy powinniśmy dopisać ``(anonymous namespace)``, jak w poniższym przykładzie:

.. code:: text

  > gdb ./a.out 
  GNU gdb (GDB) Fedora 7.12.1-41.fc25
  Copyright (C) 2017 Free Software Foundation, Inc.
  License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
  This is free software: you are free to change and redistribute it.
  There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
  and "show warranty" for details.
  This GDB was configured as "x86_64-redhat-linux-gnu".
  Type "show configuration" for configuration details.
  For bug reporting instructions, please see:
  <http://www.gnu.org/software/gdb/bugs/>.
  Find the GDB manual and other documentation resources online at:
  <http://www.gnu.org/software/gdb/documentation/>.
  For help, type "help".
  Type "apropos word" to search for commands related to "word"...
  Reading symbols from ./a.out...done.
  (gdb) b funkcja
  Function "funkcja" not defined.
  Make breakpoint pending on future shared library load? (y or [n]) n
  (gdb) break (anonymous namespace)::funkcja
  Breakpoint 1 at 0x4007aa: file anonymous-namespace.cpp, line 8.
  (gdb) quit


Jest to oczywiście jedno rozwiązanie. Inną metodą jest znalezienie nazwy funkcji w stylu C (udekorowanej - `name mangling <https://en.wikipedia.org/wiki/Name_mangling>`__) i na niej ustawienie pułapki. Nazwę funkcji możemy poznać za pomocą polecenia ``nm`` (linia 39) lub ``objdump``:

.. code:: text

  > nm a.out 
  0000000000601044 B __bss_start
  0000000000601170 b completed.6917
                   U __cxa_atexit@@GLIBC_2.2.5
  0000000000601040 D __data_start
  0000000000601040 W data_start
  00000000004006e0 t deregister_tm_clones
  0000000000400760 t __do_global_dtors_aux
  0000000000600de0 t __do_global_dtors_aux_fini_array_entry
  00000000004008c8 R __dso_handle
  0000000000600df0 d _DYNAMIC
  0000000000601044 D _edata
  0000000000601178 B _end
  00000000004008b4 T _fini
  0000000000400780 t frame_dummy
  0000000000600dd0 t __frame_dummy_init_array_entry
  0000000000400a70 r __FRAME_END__
  0000000000601000 d _GLOBAL_OFFSET_TABLE_
  0000000000400823 t _GLOBAL__sub_I_main
                   w __gmon_start__
  00000000004008d4 r __GNU_EH_FRAME_HDR
  0000000000400638 T _init
  0000000000600de0 t __init_array_end
  0000000000600dd0 t __init_array_start
  00000000004008c0 R _IO_stdin_used
                   w _ITM_deregisterTMCloneTable
                   w _ITM_registerTMCloneTable
  0000000000600de8 d __JCR_END__
  0000000000600de8 d __JCR_LIST__
                   w _Jv_RegisterClasses
  00000000004008b0 T __libc_csu_fini
  0000000000400840 T __libc_csu_init
                   U __libc_start_main@@GLIBC_2.2.5
  00000000004007b1 T main
  0000000000400720 t register_tm_clones
  00000000004006b0 T _start
  0000000000601048 D __TMC_END__
  00000000004007e5 t _Z41__static_initialization_and_destruction_0ii
  00000000004007a6 t _ZN12_GLOBAL__N_17funkcjaEv
                   U _ZNSolsEi@@GLIBCXX_3.4
                   U _ZNSt8ios_base4InitC1Ev@@GLIBCXX_3.4
                   U _ZNSt8ios_base4InitD1Ev@@GLIBCXX_3.4
  0000000000601060 B _ZSt4cout@@GLIBCXX_3.4
  00000000004008d0 r _ZStL19piecewise_construct
  0000000000601171 b _ZStL8__ioinit
                   U _ZStlsISt11char_traitsIcEERSt13basic_ostreamIcT_ES5_c@@GLIBCXX_3.4


Powyżej widać, że szukaną nazwą jest ``_ZN12_GLOBAL__N_17funkcjaEv``. W przykładzie poniżej możemy zaobserwować, że pułapka została ustawiona (linia 18), a GDB poprawnie zinterpretowało jej nazwę (linia 23):

.. code:: text

  > gdb ./a.out 
  GNU gdb (GDB) Fedora 7.12.1-41.fc25
  Copyright (C) 2017 Free Software Foundation, Inc.
  License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
  This is free software: you are free to change and redistribute it.
  There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
  and "show warranty" for details.
  This GDB was configured as "x86_64-redhat-linux-gnu".
  Type "show configuration" for configuration details.
  For bug reporting instructions, please see:
  <http://www.gnu.org/software/gdb/bugs/>.
  Find the GDB manual and other documentation resources online at:
  <http://www.gnu.org/software/gdb/documentation/>.
  For help, type "help".
  Type "apropos word" to search for commands related to "word"...
  Reading symbols from ./a.out...done.
  (gdb) b _ZN12_GLOBAL__N_17funkcjaEv
  Breakpoint 1 at 0x4007aa: file anonymous-namespace.cpp, line 8.
  (gdb) run
  Starting program: /home/achyla/.adam/tests/a.out 
  Missing separate debuginfos, use: dnf debuginfo-install glibc-2.24-4.fc25.x86_64
  
  Breakpoint 1, (anonymous namespace)::funkcja () at anonymous-namespace.cpp:8
  8           return 5;
  Missing separate debuginfos, use: dnf debuginfo-install libgcc-6.3.1-1.fc25.x86_64 libstdc++-6.3.1-1.fc25.x86_64
  (gdb) c
  Continuing.
  5
  [Inferior 1 (process 7443) exited normally]
  (gdb) quit


Literatura
----------

1. `Bug 16874 - Setting a breakpoint on function in anonymous namespace is unnecessarily awkward <https://sourceware.org/bugzilla/show_bug.cgi?id=16874>`__
2. `Stack Overflow - GCC C++ Name mangling reference <http://stackoverflow.com/questions/41524956/gcc-c-name-mangling-reference>`__
