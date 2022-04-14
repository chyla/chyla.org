(Write-Up) Misja 002 - Ukryte dane w Base64
===========================================

Write-up z misji Gynvaela Coldwinda zaprezentowanej na jednym z live streamów. Wiemy, że dane ukryto w ciągu znaków zakodowanym za pomocą Base64, odnajdźmy je!

Treść misji została zaprezentowana na końcu streamu `Pluginy, DLLki - z czym to się je <https://www.youtube.com/watch?v=FN-5CowRdXM>`__. Dla przypomnienia umieszczam ją poniżej::

  MISJA 002                                                  DIFFICULTY: [3/10]

  Przechwyciliśmy fragment komunikacji pomiędzy dwoma podejrzanymi. Sądzimy, że
  to hasło administratora do jednego z systemów, na których mogą znajdować się
  kluczowe dla sprawy dane.

                +---                                   ---+
                | QW== QT== QT== QQ== QU== Qd== QU== Qd== |
                  QX== QV== QW== Qe== QT== QR== QU== QT==
                  QT== QU== QX== QU== QT== QR== QT== QQ==
                | QW== Qe==               »goo.gl/4Iuxdi« |
                +---                                   ---+

  Niestety, pomimo, iż wiemy, że użyte zostało kodowanie Base64, nie jesteśmy w
  stanie zdekodować ukrytej wiadomości. Nasi technicy uparcie twierdzą, że po
  zdekodowaniu wychodzi „AAAAAAAAAAAAAAAAAAAAAAAAAA”, ale sądzimy, że nie mają
  racji.

  Zwracamy się więc do Ciebie z prośbą o pomoc - zrzuć okiem na powyższą
  wiadomość i sprawdź czy nie ma czasem drugiego dna.

Zastanawiające są znaki dopełnienia (=) w środku zakodowanej wiadomości, powinny być umieszczone na samym końcu. Spróbujmy jednak zdekodować podany ciąg. W linuksie dostępne jest polecenie `base64`, które wywołane z opcją `-d` pozwala wykonać dekodowanie::

  $ cat > enc
  QW== QT== QT== QQ== QU== Qd== QU== Qd==
  QX== QV== QW== Qe== QT== QR== QU== QT==
  QT== QU== QX== QU== QT== QR== QT== QQ==
  QW== Qe==

  $ base64 -d enc
  Abase64: błędne dane wejściowe

  $ base64 -d enc 2> /dev/null
  A

Nie udało się, jednak według informacji podanej w treści misji powinniśmy otrzymać litery `A`. Pójdźmy tropem związanym ze znakami dopełnienia i potraktujmy każdą z grup jako osobny ciąg do zdekodowania::

  $ for group in $(cat enc) ; do base64 -d <<< $group ; done
  AAAAAAAAAAAAAAAAAAAAAAAAAA

Teraz otrzymaliśmy ciąg podany w treści zadania. Chyba jesteśmy o krok dalej. Myślę, że możemy każdą grupę traktować jako osobny ciąg do zdekodowania.

Zobaczmy też, jak wygląda wynik dekodowania jednej grupy po przekazaniu do programu `hexdump`. Może na terminalu otrzymaliśmy znaki niedrukowalne::

  $ base64 -d <<< QW== | hexdump
  0000000 0041
  0000001

Nie ma tam nic ciekawego, tylko znak ``A``. Zdekodujmy więc sami pierwszą grupę. Jest to operacja odwrotna do kodowania, którego na `Wikipedii <https://pl.wikipedia.org/wiki/Base64>`__ znalazłem dość jasny opis:

  Kodowanie to przypisuje 64 wybranym znakom (patrz tabelka niżej) wartości od 0 do 63. Ciąg bajtów poddawany kodowaniu dzielony jest na grupy po 3 bajty. Ponieważ bajt ma 8 bitów, grupa 3 bajtów składa się z 24 bitów. Każdą taką grupę dzieli się następnie na 4 jednostki 6-bitowe. Istnieją więc dokładnie 64 możliwe wartości każdej takiej jednostki. Wszystkim tym jednostkom są przypisywane znaki na podstawie arbitralnie ustalonego przypisania (patrz tabela poniżej).

  Jeśli rozmiar wejściowego ciągu bajtów nie jest wielokrotnością liczby 3, to stosowane jest dopełnianie (na końcu wynikowego ciągu dodawana jest taka ilość symboli dopełnienia (pad), aby ten miał długość podzielną przez 3).


Dekodowanie będzie polegało na zamianie liter na wartości w formie binarnej, połączeniu całości w grupy i wyodrębnieniu każdego z bajtów.

Zaczynamy od grupy ``QW==``. Litera ``Q`` ma wartość 16, a litera ``W`` - 22, ``=`` to dopełnienie. Zapiszmy to binarnie::

  010000  010110

Podane wartości w formie binarnej zajmują 5 miejsc, a do wykorzystania mamy 6, dlatego zostały uzupełnione z przodu jednym zerem.

Teraz przegrupujmy otrzymane bity, by móc odczytać pierwszy bajt::

  01000001 0110

Z tablicy `ASCII <https://pl.wikipedia.org/wiki/ASCII>`__ możemy odczytać, że pierwszy bajt jest reprezentowany jako litera ``A``. Jest to znak, który udało nam się wcześniej zdekodować za pomocą programu ``base64``. Widzimy jednak teraz, że znajdują się tutaj dodatkowe dane (``0110``), które nie zostały wyświetlone. Nie tworzą one całego bajtu i zostały pominięte.

Pomyślmy przez chwilę co z dopełnieniem. Wikipedia niewiele mówi na ten temat, dlatego trzeba rzucić okiem na `specyfikację <https://tools.ietf.org/html/rfc4648#section-3.5>`__ (szukamy po słowie padding):

  The padding step in base 64 and base 32 encoding can, if improperly
  implemented, lead to non-significant alterations of the encoded data.
  For example, if the input is only one octet for a base 64 encoding,
  then all six bits of the first symbol are used, but only the first
  two bits of the next symbol are used.  These pad bits MUST be set to
  zero by conforming encoders, which is described in the descriptions
  on padding below.  If this property do not hold, there is no
  canonical representation of base-encoded data, and multiple base-
  encoded strings can be decoded to the same binary data.  If this
  property (and others discussed in this document) holds, a canonical
  encoding is guaranteed.

  In some environments, the alteration is critical and therefore
  decoders MAY chose to reject an encoding if the pad bits have not
  been set to zero.


Wygląda na to, że opisany jest przypadek, który nas interesuje. Odczytajmy zatem wszystkie dodatkowe dane. Wystarczy, że na wejście podamy litery znajdujące się po literze ``Q`` w każdej z grup. Z nich będziemy mogli odkryć ukryte dane zamieniając je na liczby 6-bitowe i wybierając dolne 4 bity.

Kolejne litery, które zawierają ukryte dane::

  $ cat enc | tr ' ' '\n' | sed -r 's/.(.).*/\1/' | tr -d '\n'
  WTTQUdUdXVWeTRUTTUXUTRTQWe

Zobaczmy program:

.. code:: cpp

  #include <iostream>
  #include <array>
  #include <unordered_map>

  using namespace std;

  array<char, 26> data = {
  	'W', 'T', 'T', 'Q', 'U', 'd', 'U', 'd', 'X', 'V', 'W', 'e', 'T',
  	'R', 'U', 'T', 'T', 'U', 'X', 'U', 'T', 'R', 'T', 'Q', 'W', 'e'
  };

  unordered_map<char, char> b64_map {
      {'d', 29},
      {'e', 30},
      {'R', 17},
      {'Q', 16},
      {'T', 19},
      {'U', 20},
      {'V', 21},
      {'W', 22},
      {'X', 23}
  };

  void print_bits(char part, char bits) {
  	cout << "Bits for " << part << ": "
  		<< bool(bits & 0x08) << " "
  		<< bool(bits & 0x04) << " "
  		<< bool(bits & 0x02) << " "
  		<< bool(bits & 0x01) << "\n";
  }

  int main() {
  	for (char c : data) {
  		print_bits(c, b64_map.at(c));
  	}
  	return 0;
  }


I jego wynik prezentujący wszystkie ukryte dane w kolejności ich występowania::

  Bits for W: 0 1 1 0
  Bits for T: 0 0 1 1
  Bits for T: 0 0 1 1
  Bits for Q: 0 0 0 0
  Bits for U: 0 1 0 0
  Bits for d: 1 1 0 1
  Bits for U: 0 1 0 0
  Bits for d: 1 1 0 1
  Bits for X: 0 1 1 1
  Bits for V: 0 1 0 1
  Bits for W: 0 1 1 0
  Bits for e: 1 1 1 0
  Bits for T: 0 0 1 1
  Bits for R: 0 0 0 1
  Bits for U: 0 1 0 0
  Bits for T: 0 0 1 1
  Bits for T: 0 0 1 1
  Bits for U: 0 1 0 0
  Bits for X: 0 1 1 1
  Bits for U: 0 1 0 0
  Bits for T: 0 0 1 1
  Bits for R: 0 0 0 1
  Bits for T: 0 0 1 1
  Bits for Q: 0 0 0 0
  Bits for W: 0 1 1 0
  Bits for e: 1 1 1 0

Niewiele to pomogło. Zadanie jest jednak ocenione jako dość proste, spróbujmy więc pogrupować bity po 8 i każdą z grup (czyli bajt) zamienić na znak ASCII.

.. code:: cpp

  #include <iostream>
  #include <array>
  #include <unordered_map>

  using namespace std;

  array<char, 26> data = {
  	'W', 'T', 'T', 'Q', 'U', 'd', 'U', 'd', 'X', 'V', 'W', 'e', 'T',
  	'R', 'U', 'T', 'T', 'U', 'X', 'U', 'T', 'R', 'T', 'Q', 'W', 'e'
  };

  unordered_map<char, char> b64_map {
      {'d', 29},
      {'e', 30},
      {'R', 17},
      {'Q', 16},
      {'T', 19},
      {'U', 20},
      {'V', 21},
      {'W', 22},
      {'X', 23}
  };

  void print_ascii(char b1, char b2) {
  	char higher_bits = b1 << 4;
  	char lower_bits = b2 & 0x0F;

  	char result = higher_bits | lower_bits;

  	cout << result;
  }

  int main() {
  	for (int i = 0; i < data.size(); i += 2) {
  		print_ascii(b64_map.at(data[i]), b64_map.at(data[i+1]));
  	}
  	return 0;
  }


Wynik działania programu::

  c0MMun1C4t10n

Rozwiązanie znalezione ☺

.. note::

    `Gynvael Coldwind <http://gynvael.coldwind.pl>`__ udostępnił film `Gynvael's Livestream #39: RPC, czyli zdalne API <https://youtu.be/xR0hAJPp1vs?t=460>`__, na którym przedstawia swoje oraz omawia nadesłane rozwiązania.
