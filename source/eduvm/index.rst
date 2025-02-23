EduVM
=====

Maszyna wirtualna `VirtualBox <https://www.virtualbox.org/>`__ z zainstalowanym
`Xubuntu <https://xubuntu.org/>`__ wraz z narzędziami programistycznymi
dla Pythona i C++. Zawiera tylko wolne oprogramowanie, zgodne z założeniami
`DFSG <https://www.debian.org/social_contract#guidelines>`__ (sprawdzane
za pomocą `check-dfsg-status - vrms <https://debian.pages.debian.net/check-dfsg-status/>`__).

W maszynie wirtualnej znajdziesz:

* interpreter języka Python 3 (CPython);
* kompilator języka C++ (GCC, Clang);
* środowiska programistyczne:

  * PyCharm Community,
  * Microsoft Visual Studio Code (ze względów licencyjnych nie jest bezpośrednio
    zainstalowany, lecz jest pobierany przy pierwszej próbie uruchomienia);
  * Qt Creator,
  * KDevelop,

* narzędzia Python (np. venv, virtualenv, pyenv, black, flake8, pylint, pycodestyle);
* narzędzia C++ (np. GDB, cmake, ninja, KCachegrind, Cppcheck, gcovr, GoogleTest);

Pełną listę oraz wersje poszczególnych pakietów znajdziesz na stronie wydania.


Pobieranie
----------

Do pobrania maszyny wirtualnej potrzebujesz klienta BitTorrent ze wsparciem
dla *webseeding*. Klient BitTorrent zadba o poprawne pobranie
pliku - w przypadku błędów podczas transmisji danych, tylko niepoprawny
fragment pliku zostanie pobrany ponownie. **Polecam** `qBittorrent <https://www.qbittorrent.org/download>`__.
**Odradzam** `Transmission <https://transmissionbt.com/>`__,
gdyż w niektórych przypadkach `nie rozpoczyna pobierania <https://github.com/transmission/transmission/issues/3705>`__.

Po zainstalowaniu klienta otwórz plik ``.torrent`` (dostępny w sekcji
*Wydania*), aby rozpocząć pobieranie.

Wskazówka: *Nie ograniczaj prędkości wysyłania danych, od niej również
zależy prędkość pobierania danych.*


Wydania
-------

.. toctree::
    :maxdepth: 1

    2410/index
    2404/index
    2310/index
    2304/index
