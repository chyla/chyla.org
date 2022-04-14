SQLite - Włączenie weryfikacji Foreign Key Constraints
======================================================

Foreign Key Constraints pozwala zachować spójność bazy danych poprzez weryfikację powiązań pomiędzy tabelami. O ile większość programistów wie po co są klucze obce i jak je oznaczać, o tyle już nie każdy musi wiedzieć, że w SQLite opcja ta (nawet poprawnie oznaczona przez programistę) jest domyślnie wyłączona. Do jej włączenia niezbędne jest wykonanie odpowiedniego polecenia PRAGMA.

Zależność pomiędzy tabelami opisujemy za pomocą kluczy obcych. Jeśli w tabeli B utworzymy klucz obcy wskazujący na kolumnę tabeli A, przy włączonej weryfikacji, utworzenie nowego rekordu w tabeli B odwołującego się do nieistniejącego rekordu w tabeli A nie powinno się powieść. Domyślnie SQLite pozwala na takie zachowanie. Można to zmienić za pomocą polecenia:

.. code:: sql

    PRAGMA foreign_keys = on;

Wykonanie polecenia spowoduje włączenie weryfikacji zależności, ale tylko w obrębie obecnego połączenia. Nie jest to ustawienie trwałe, co obrazuje poniższy przykład:

.. code:: sql

  # sqlite3 /tmp/ex.db
  SQLite version 3.8.7.1 2014-10-29 13:59:56
  Enter ".help" for usage hints.
  sqlite> PRAGMA foreign_keys = on;
  sqlite> CREATE TABLE names (id INTEGER PRIMARY KEY NOT NULL, name TEXT, UNIQUE (name) );
  sqlite> CREATE TABLE phones (id INTEGER PRIMARY KEY NOT NULL, name_id INTEGER, phone TEXT, foreign key(name_id) references names(id) );
  sqlite> insert into phones values (1, 1, "123456789");
  Error: FOREIGN KEY constraint failed
  sqlite> -- blad - w tabeli names nie ma wpisu o id = 1
  sqlite> .quit
  
  # sqlite3 /tmp/ex.db
  SQLite version 3.8.7.1 2014-10-29 13:59:56
  Enter ".help" for usage hints.
  sqlite> insert into phones values (1, 1, "123456789");
  sqlite> .quit

W nowych aplikacjach ustawienie to powinno być zawsze włączone (z raczej dość oczywistych powodów) przez programistę, w końcu jak informuje dokumentacja `[1] <#literatura>`__: *To minimize future problems, applications should set the foreign key enforcement flag as required by the application and not depend on the default setting.*

Kontrola integralności rekordów w tabelach nie jest jedyną zaletą stosowania kluczy obcych, w końcu pozwalają między innymi definiować akcje ON DELETE i ON UPDATE.


Literatura
----------

1. `PRAGMA Statements <https://www.sqlite.org/pragma.html#pragma_foreign_keys>`__
2. `SQLite Foreign Key Support <https://www.sqlite.org/foreignkeys.html>`__
