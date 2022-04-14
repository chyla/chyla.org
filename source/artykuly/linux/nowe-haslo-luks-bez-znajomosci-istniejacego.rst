Nowe hasło LUKS bez znajomości istniejącego
===========================================

Za Wikipedią:

  Linux Unified Key Setup (LUKS) – specyfikacja szyfrowania dysku twardego stworzona przez Clemensa Fruhwirtha i oryginalnie przeznaczona dla Linuksa.

  Podczas gdy większość oprogramowania do szyfrowania dysków implementuje różne i niekompatybilne, nieudokumentowane formaty, LUKS wyznacza niezależny od platformy systemowej standard dla użytku w różnorodnych programach i narzędziach. To nie tylko ułatwia kompatybilność i wymienialność pomiędzy różnymi programami, ale również zapewnia, że wszystkie programy używające LUKS implementują zarządzanie hasłami w bezpieczny i udokumentowany sposób.

  Ustandaryzowana implementacja dla LUKS działa na Linuksie i jest oparta na rozszerzonej wersji cryptsetup, używającej dm-crypt jako narzędzia do szyfrowania dysku. Pod systemem Microsoft Windows dyski zaszyfrowane przy pomocy LUKS mogą być używane przy pomocy FreeOTFE.

LUKS umożliwia ustawienie kilku haseł dla zaszyfrowanego kontenera (dysku, partycji, pliku). Każde hasło pozwala na odszyfrowanie pewnej powiązanej z nim porcji danych. Ta porcja danych to zaszyfrowany klucz główny umieszczony w specjalnym miejscu nazywanym slotem.

Każde z haseł ustala użytkownik — jest to ten element, który musi zostać podany w procesie tworzenia oraz otwierania zaszyfrowanego kontenera. Klucz główny natomiast jest ustalany losowo podczas tworzenia zaszyfrowanego kontenera i jest on tylko jeden.

Użytkownik, podając jedno z haseł, umożliwia oprogramowaniu odszyfrowanie klucza głównego. Następnie za pomocą tego klucza głównego szyfrowane/deszyfrowane są dane w kontenerze.

Klucz główny, w przeciwieństwie do hasła, wymagany jest przez cały czas pracy z zaszyfrowanym kontenerem. Z tego powodu jest on umieszczony w pamięci komputera, a zatem jest możliwy do odczytania. `cryptsetup` dostarcza odpowiednich narzędzi do tego celu.

Klucz główny w postaci szesnastkowej możemy odczytać za pomocą polecenia::

  dmsetup table --showkeys <nazwa_kontenera>


Co zrobić, aby utworzyć nowe hasło? Należy zaszyfrować binarną formę klucza głównego i umieścić ją w odpowiednim slocie.

W tym celu skonwertujmy klucz główny z zapisu szesnastkowego do postaci binarnej i zapiszmy go do pliku::

  dmsetup table --showkeys <nazwa_kontenera> | awk '{ print $5 }' | xxd -r -p > binary_key


Mając klucz główny, użyjemy go do utworzenia nowego hasła::

  cryptsetup luksAddKey <nazwa_kontenera> --master-key-file binary_key


W ten sposób dodaliśmy nowe hasło do kontenera, którego stare hasło zaginęło.


Literatura
----------

1. `Linux Unified Key Setup <https://pl.wikipedia.org/wiki/Linux_Unified_Key_Setup>`__
2. `Change password on a LUKS filesystem without knowing the password <https://unix.stackexchange.com/questions/161915/change-password-on-a-luks-filesystem-without-knowing-the-password>`__
