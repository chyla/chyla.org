Dowiązanie w systemie plików a AV i Linux
=========================================


Wstęp
-----

Bardzo ogólnie mówiąc, dowiązanie jest dodatkową nazwą (w systemie plików) na plik lub katalog. Z punktu widzenia użytkownika, różnice pomiędzy dowiązaniem a zwykłym plikiem są niemal niezauważalne — wszelkie operacje są wykonywane na oryginalnym pliku/katalogu.

Możemy wyróżnić trzy rodzaje dowiązań:

- miękkie,
- twarde,
- directory junction.

Pierwsze dwa to klasyczne dowiązania znane ze środowiska uniksowego. Trzecie natomiast, dostępne jest tylko w systemach Windows (od 2000).

Dowiązanie miękkie (inaczej dowiązanie symboliczne, link symboliczny) jest plikiem przechowującym alternatywną ścieżkę do pliku docelowego. Plikiem docelowym może być plik/katalog (także nieistniejący) lub plik/katalog znajdujący się w innym systemie plików.

Dowiązanie twarde jest bezpośrednim wskazaniem na i-węzeł znajdujący się wyłącznie w obrębie tego samego systemu plików.

Wskazane różnice pomiędzy dowiązaniem miękkim a twardym zostały przez Iana Shieldsa opisane następująco:

    A hard link is a directory entry that points to an inode, while a soft link or symbolic link is a directory entry that points to an inode that provides the name of another directory entry. The exact mechanism for storing the second name may depend on both the file system and the length of the name. [`Ian Shields, Create and change hard and symbolic links <https://www.ibm.com/developerworks/library/l-lpic1-v3-104-6/index.html>`__]

Directory junction jest dowiązaniem zaimplementowanym za pomocą "reparse points". Może wskazywać wyłącznie na katalogi w obrębie danego systemu operacyjnego (podobnie jak dowiązanie miękkie). Harry Johnston przedstawił różnice między directory junction a dowiązaniem miękkim następująco:

    The main difference is that, if you are looking at a remote server, **junctions are processed at the server** and **directory symbolic links are processed at the client**. [`Harry Johnston <https://superuser.com/a/343079>`__]


Podatność #AVGater
------------------

#AVGater bazuje na koncepcji dowiązań, by podwyższyć uprawnienia użytkownika aż do uprawnień administratora. Jak podaje Florian Bogner (odkrywca luki), podatnych na atak jest co najmniej sześć programów antywirusowych działających pod kontrolą systemu Windows — Kaspersky, Trend Micro, Emsisoft, Malwarebytes, Zone Alarm, Ikarus.

.. figure:: /images/artykuly/linux/dowiazanie-w-systemie-plikow-a-av-i-linux-avgater-logo-small.png

    Logo podatności. Źródło: [6]

Błąd znajduje się w mechanizmie przywracania plików z kwarantanny — oprogramowanie nie weryfikuje, czy miejsce docelowe jest dowiązaniem. Przebieg ataku jest następujący:

1. Oprogramowanie antywirusowe umieszcza, wybrany przez atakującego, plik w kwarantannie.
2. Atakujący usuwa katalog, w którym znajdował się plik, a w jego miejsce tworzy dowiązanie (konkretnie directory junction) do innej lokalizacji (np. C:\\Windows, C:\\Windows\\System32). Oprogramowanie antywirusowe przywraca plik do katalogu źródłowego, który teraz jest dowiązaniem.
3. Inne oprogramowanie ładuje wybrany przez atakującego plik (może to być biblioteka dynamiczna, która zostanie załadowana automatycznie podczas uruchamiania programu).

.. figure:: /images/artykuly/linux/dowiazanie-w-systemie-plikow-a-av-i-linux-avgater-summary.png

   Schemat przedstawiający przebieg ataku. Źródło: [6]

Do momentu poprawienia luki w oprogramowaniu antywirusowym, zalecane jest zablokowanie użytkownikom funkcji przywracania plików z kwarantanny.


Z podręcznika administratora
----------------------------

Pomysł na atak wykorzystujący dowiązania nie jest nowy. W podręcznikach dla administratorów omawiane są przykładowe scenariusze wraz z metodami obrony.

W 2003 roku Bri Hatch przedstawił następującą historię [8]:

    Atakującemu udało się dostać do zabezpieczonego systemu, uzyskał prawa zwykłego użytkownika i mógł wykonywać polecenia konsoli. System był jednak stale aktualizowany i atakujący nie mógł podwyższyć swoich uprawnień stosując znane luki w oprogramowaniu.

    Po kilku miesiącach, w pewnym programie uruchamianym z uprawnieniami administratora, wykryto błąd pozwalający na wykonanie dowolnego polecenia. Oczywiście administrator zaktualizował wadliwe oprogramowanie, jednak po kilku dniach okazało się, że mimo aktualizacji luka została wykorzystana. Administrator usunął w całości wadliwe oprogramowanie, po czym ponownie je zainstalował, a mimo to atakujący w dalszym ciągu wykorzystywał wykrytą lukę.

Jak to możliwe, co przeoczył administrator? W grudniu 2003 roku Bri Hatch udostępnił rozwiązanie tej zagadki [9].

Kluczem do sukcesu atakującego okazała się wiedza na temat dowiązania twardego. Dowiązanie tego typu zachowuje wszelkie atrybuty (np. bit suid) - są one przechowywane z i-węzłem. Co więcej, usunięcie oryginalnego pliku (de facto dowiązania twardego) nie oznacza, że dany plik został usunięty - jest to jedynie usunięcie pierwotnej nazwy, pierwotnego dowiązania.

Atakujący utworzył dowiązanie twarde do podatnej aplikacji w katalogu `/tmp`, co spowodowało, że pomimo aktualizacji w jego rękach ciągle znajdowała się niezaktualizowana wersja oprogramowania. Zachęcam do zapoznania się z całym opisem tej historii oraz jej rozwiązaniem.

Jedną z metod ochrony przed tego typu atakiem jest umieszczenie katalogów, do których prawa zapisu ma użytkownik, na osobnych systemach plików. Zabieg ten uniemożliwia tworzenie dowiązań twardych. Innym rozwiązaniem jest zastosowanie odpowiedniej modyfikacji jądra (np. OpenWall) blokującej tworzenie dowiązań twardych do plików, których użytkownik nie jest właścicielem [7].


Znane podatności w systemie Linux
---------------------------------

Przypadków wykorzystania błędów związanych z dowiązaniami jest więcej. Przeszukując bazę CVE (Common Vulnerabilities and Exposures), pod kątem błędów powiązanych z samymi dowiązaniami twardymi [10], otrzymujemy 41 wyników (na dzień 15.11.2017). Błędy te dotyczą różnego oprogramowania, jednak dwa z nich wydają się szczególnie ciekawe.

.. figure:: /images/artykuly/linux/dowiazanie-w-systemie-plikow-a-av-i-linux-cve-search.png

    Fragment wyników wyszukiwania "hard link" w bazie Common Vulnerabilities and Exposures. [10]

Wybrane podatności dotyczą menadżerów pakietów rpm oraz dpkg, co sprawia, że wpływa to na bezpieczeństwo dystrybucji na nich opartych (np. Ubuntu, Debian, Fedora). Co ciekawsze, są one związane z historią przedstawioną powyżej. Oczywiście odpowiednie poprawki zostały wdrożone i problem już nie występuje.

Podatność związana z menadżerem pakietów **dpkg** z **2004** roku:

    dpkg 1.9.21 does not properly reset the metadata of a file during replacement of the file in a package upgrade, which might allow local users to gain privileges by creating a hard link to a vulnerable (1) setuid file, (2) setgid file, or (3) device, a related issue to CVE-2010-2059. `[źródło: CVE] <http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2004-2768>`__

Podatność związana z menadżerem pakietów **rpm** z **2010** roku:

    lib/fsm.c in RPM 4.8.0 and earlier does not properly reset the metadata of an executable file during replacement of the file in an RPM package upgrade or deletion of the file in an RPM package removal, which might allow local users to gain privileges or bypass intended access restrictions by creating a hard link to a vulnerable file that has (1) POSIX file capabilities or (2) SELinux context information, a related issue to CVE-2010-2059. `[źródło: CVE] <http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2010-2198>`__

Błędy związane z dowiązaniami są znane, a mimo to ciągle popełniane. Warto o nich pamiętać i co jakiś czas sprawdzać aplikacje pod kątem ich występowania.


Literatura
----------

1. `Ian Shields, Create and change hard and symbolic links <https://www.ibm.com/developerworks/library/l-lpic1-v3-104-6/index.html>`__
2. `Hard Links and Junctions <https://msdn.microsoft.com/en-us/library/windows/desktop/aa365006%28v=vs.85%29.aspx?f=255&MSPPError=-2147217396>`__
3. `Reparse Points <https://msdn.microsoft.com/en-us/library/windows/desktop/aa365503(v=vs.85).aspx>`__
4. `“directory junction” vs “directory symbolic link”? <https://superuser.com/questions/343074/directory-junction-vs-directory-symbolic-link>`__
5. `Linki symboliczne w Windows umożliwiły otrzymanie lokalnego admina na popularnych antywirusach <https://sekurak.pl/linki-symboliczne-w-windows-umozliwily-otrzymanie-lokalnego-admina-na-popularnych-antywirusach/>`__
6. `#AVGater: Getting Local Admin by Abusing the Anti-Virus Quarantine » #bogner.sh <https://bogner.sh/2017/11/avgater-getting-local-admin-by-abusing-the-anti-virus-quarantine/>`__
7. `Turnbull, J. (2006), Hardening Linux, s. 68 <https://books.google.pl/books?id=PyqjvNNltqYC&pg=PA68&lpg=PA68&dq=linux+hard+link+attack&source=bl&ots=XFiFcyTC6L&sig=4TCRTdQuQxQak5TNtocrXA2ekQc&hl=pl&sa=X&ved=0ahUKEwim6q7Nn7rXAhWLLcAKHQgZDesQ6AEIcjAJ#v=onepage&q&f=false>`__
8. `Contest - The mysteriously persistently exploitable program <https://www.hackinglinuxexposed.com/articles/20031111.html>`__
9. `[ISN] The mysteriously persistently exploitable program explained. <http://lists.jammed.com/ISN/2003/12/0056.html>`__
10. `hard link - CVE - Search Results <http://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=hard+link>`__
11. `dpkg does not properly reset the metadata (CVE-2004-2768) <http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2004-2768>`__
12. `rpm does not properly reset the metadata (CVE-2010-2198) <http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2010-2198>`__
