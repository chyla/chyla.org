OpenSSH - Kody kontrolne, klucze, multiplexing, proxyjump
=========================================================


Spis treści
-----------

1. Kody kontrolne - ratunku, to połączenie umarło!
2. Klucze SSH - logowanie bez hasła
3. Multiplexing - jeden bezpieczny kanał komunikacji dla wszystkich sesji
4. ProxyJump - dostęp do systemu w sieci wewnętrznej za pomocą systemu pośredniczącego


Kody kontrolne
--------------

Podczas sesji SSH ze zdalnym serwerem, czasami, dochodzi do sytuacji, w której nie jesteśmy w stanie nic zrobić. Klawiatura nie odpowiada, a wpisywane znaki nie pojawiają się na ekranie - to połączenie umarło! bo Wi-Fi zgubiło zasięg, a my nie używamy `Mosha <https://mosh.org/>`__... gdyby tak móc powrócić do terminala...

Jest na to rada - trzeba zamknąć to połączenie. Jak? Bardzo prosto, w trzech krokach:

* `ENTER`
* `~`
* `.`

Tak, wystarczy na klawiaturze nacisnąć po kolei `ENTER` `~` `.` - połączenie powinno zostać zamknięte, a my odzyskamy dostęp do terminala.

OpenSSH obsługuje kody kontrolne (escape codes) - specjalne polecenia dla dodatkowej kontroli programu. Polecenie takie zawsze zaczyna się od znaku tyldy, warto jednak zwrócić uwagę na dodatkowy `ENTER`. Kody kontrolne rozpoznawane są tylko wtedy, gdy występują bezpośrednio po znaku nowej linii (przykład: gdyby tak nie było, to mielibyśmy utrudnione użycie `~` jako odniesienia do katalogu domowego).

Pełną listę dostępnych sekwencji znajdziemy w pomocy... Ach tak, `ENTER` `~` `?`, polecam lekturę::

  Supported escape sequences:
   ~.   - terminate connection (and any multiplexed sessions)
   ~B   - send a BREAK to the remote system
   ~C   - open a command line
   ~R   - request rekey
   ~V/v - decrease/increase verbosity (LogLevel)
   ~^Z  - suspend ssh
   ~#   - list forwarded connections
   ~&   - background ssh (when waiting for connections to terminate)
   ~?   - this message
   ~~   - send the escape character by typing it twice
  (Note that escapes are only recognized immediately after newline.)


Klucze SSH
----------

Zwykle, przy nawiązywaniu połączenia, musimy podać hasło. Ten krok można jednak ominąć i zamiast hasła użyć klucza kryptograficznego. Na jego podstawie nastąpi automatyczne uwierzytelnienie, bez naszego udziału.

Czego potrzebujemy?

* wygenerowanej pary kluczy kryptograficzne - klucz publiczny i prywatny
* jednorazowej wymiany klucza publicznego ze zdalną maszyną

Wygenerowane klucze możemy znaleźć w katalogu `~/.ssh/` - zazwyczaj są to pliki `id_rsa` dla klucza prywatnego oraz `id_rsa.pub` dla klucza publicznego::

  $ ls  ~/.ssh
  id_rsa  id_rsa.pub

Jeżeli ich nie mamy, możemy wygenerować je poleceniem `ssh-keygen`::

  $ ls -al ~/.ssh
  ls: nie ma dostępu do '/home/adam/.ssh': Nie ma takiego pliku ani katalogu

  $ ssh-keygen
  Generating public/private rsa key pair.
  Enter file in which to save the key (/home/adam/.ssh/id_rsa):
  Created directory '/home/adam/.ssh'.
  Enter passphrase (empty for no passphrase):
  Enter same passphrase again:
  Your identification has been saved in /home/adam/.ssh/id_rsa.
  Your public key has been saved in /home/adam/.ssh/id_rsa.pub.
  The key fingerprint is:
  SHA256:wqKevwDql3zwvHHImIcP3zNS1L8Nyaj4xfhbpfh/4qk adam@Host
  The key's randomart image is:
  +---[RSA 2048]----+
  |                 |
  |                 |
  |        .        |
  |     . . .       |
  |.   . + S + ..   |
  |.. o=..oo..=o    |
  |. +===oo.+ o+    |
  |.. *=*++o o. o.. |
  | .+.+=+ooo.E++o  |
  +----[SHA256]-----+

Podczas tego procesu zostaniemy zapytani o hasło dla klucza. Będziemy o nie pytani za każdym razem, gdy spróbujemy danego klucza użyć. Nie do końca o to nam chodzi, w końcu chcemy logować się bez podawania hasła, dlatego z pełną odpowiedzialnością pomijamy to pytanie naciskając klawisz `ENTER`.

Drugim krokiem jest umieszczenie klucza publicznego na zdalnym serwerze. Wykonamy to za pomocą polecenia `ssh-copy-id` - dopisze ono zawartość naszego pliku `id_rsa.pub` do `~/.ssh/authorized_keys` na zdalnym serwerze (ten krok możemy także wykonać ręcznie)::

  $ ssh-copy-id adam@ZdalnySerwer
  /usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
  /usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
  adam@ZdalnySerwer's password:

  Number of key(s) added: 1

  Now try logging into the machine, with:   "ssh 'adam@ZdalnySerwer'"
  and check to make sure that only the key(s) you wanted were added.

Od tego momentu możemy nawiązać połączenie SSH bez podawania hasła - do uwierzytelnienia zostaną wykorzystane klucze kryptograficzne. Zdalna maszyna, za pomocą klucza publicznego, zaszyfruje pewien ciąg danych, po czym wyśle go do naszej maszyny. Klient SSH, za pomocą klucza prywatnego, odszyfruje otrzymany ciąg i prześle go z powrotem do serwera, który sprawdzi poprawność otrzymanych danych.


Multiplexing
------------

Tworząc nową sesję SSH, ze zdalnym serwerem, musi zostać nawiązane bezpieczne połączenie, a to jak wiadomo trwa (np. nawiązanie połączenia TCP, autoryzacja). Warto skonfigurować `multipleksing <https://pl.wikipedia.org/wiki/Multipleksowanie>`__, czyli wykorzystywanie istniejącego, bezpiecznego kanału komunikacji podczas nawiązywania kolejnych sesji.

Odpowiednich zmian musimy dokonać w pliku konfiguracyjnym `~/.ssh/config`::

  Host *
       ControlMaster   auto
       ControlPersist  10m
       ControlPath     ~/.ssh/sockets/%r@%h:%p

Pierwsza linia informuje, że zdefiniowane niżej trzy parametry będą dotyczyły każdego połączenia.

* `ControlMaster` włącza multipleksing
* `ControlPersist` określa czas, przez który połączenie ma zostać podtrzymane, po zakończończeniu ostatniej sesji
* `ControlPath` określa ścieżkę do gniazda kontrolnego


ProxyJump
---------

Mając dostęp do tylko jednego serwera wystawionego na świat możemy uzyskać dostęp do pozostałych systemów w zamkniętej sieci. `ProxyJump` pozwala na nawiązanie połączenia z dowolnym serwerem za pomocą pośrednika.

Załóżmy, że chcemy nawiązać połączenie z serwerem o nazwie `Intra` - znajduje się on wewnątrz zamkniętej sieci, dostęp do tej sieci otrzymujemy poprzez system o nazwie `Gate`.

.. figure:: /images/artykuly/linux/openssh-kody-kontrolne-klucze-ssh-multiplexing-proxyjump-schemat-sieci.png

            Ilustracja 1: Schemat sieci.

Połączenie od naszego hosta do systemu `Intra` możemy nawiązać za pomocą polecenia::

  ssh -J user@gate user@intra

Gdy często łączymy się z hostem `Intra` warto rozważyć dodatkową konfigurację (`~/.ssh/config`), która uprości proces::

  Host intra
       HostName  intra
       ProxyJump user@gate:22
       User      user

Z powyższą konfiguracją, polecenie nawiązania połączenia z hostem `Intra` jest następujące::

  ssh intra

Starsze wersje OpenSSH nie obsługują komendy `ProxyJump`, dlatego zamiast niej stosowano `ProxyCommand` [4, 5].


Literatura
----------

1. `SSH Essentials: Working with SSH Servers, Clients, and Keys <https://www.digitalocean.com/community/tutorials/ssh-essentials-working-with-ssh-servers-clients-and-keys>`__
2. `https://en.wikibooks.org/wiki/OpenSSH/Cookbook/Multiplexing <https://en.wikibooks.org/wiki/OpenSSH/Cookbook/Multiplexing>`__
3. `SSH_CONFIG(5) <http://man.openbsd.org/ssh_config.5>`__
4. `OpenSSH/Cookbook/Proxies and Jump Hosts <https://en.wikibooks.org/wiki/OpenSSH/Cookbook/Proxies_and_Jump_Hosts>`__
5. `Zdalny dostępu do sieci wewnętrznej przy użyciu protokołu SSH <http://blog.stelmisoft.pl/2010/zdalny-dostepu-do-sieci-wewnetrznej-przy-uzyciu-protokolu-ssh/>`__
