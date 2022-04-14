Vim - Zaawansowany edytor tekstu
================================


Spis treści
-----------

0. Wstęp - instalacja Vim
1. Podstawowe polecenia - omówienie działania edytora z listą przydatnych skrótów klawiszowych
2. Dystrybucje - gotowe konfiguracje Vim

   * Instalacja space-vim
   * Konfiguracja - dostosowanie space-vim do naszych potrzeb

     * Warstwy
     * Klasyczne skróty klawiszowe (CTRL-C itp.)
     * Aliasy na literówki w poleceniach (np. `:Wq` zapisze bufor i opuści edytor)


Wstęp
-----

Przed przystąpieniem do pracy z edytorem Vim musimy upewnić się, że jest on zainstalowany w naszym systemie. Edytor można pobrać ze `strony domowej projektu <http://www.vim.org/download.php>`__ - dostępne są m.in. wersje dla Windows, Unix oraz Mac.

.. figure:: /images/artykuly/linux/vim-download.png

            Pobieranie edytora na stronie domowej projektu.

W systemie Linux najwygodniejszym sposobem jest instalacja pakietu przygotowanego przez opiekunów dystrybucji. W tych bazujących na Debianie należy zainstalować pakiet `vim` oraz `vim-gtk` (dla trybu graficznego), natomiast w dystrybucjach bazujących na RHEL/Fedora pakiety to `vim-enhanced` oraz `vim-X11` odpowiednio.


Podstawowe polecenia
--------------------

Po instalacji Vim nie zachwyca. Na pewno nie zachwyca nowych użytkowników - ani pod względem obsługi, ani pod względem wyglądu. Co prawda dostępny jest tutorial (polecenie konsoli: `vimtutor`) prezentujący podstawowe polecenia edytora, jednak próg wejścia, w możliwość swobodnego poruszania się, jest nadal wysoki.

.. figure:: /images/artykuly/linux/vim-konsola.png

            Vim uruchomiony w oknie konsoli.

.. figure:: /images/artykuly/linux/vim-gtk.png

            Vim uruchomiony z wykorzystaniem graficznego interfejsu.

Po uruchomieniu Vim działa w trybie `NORMAL`, jest to tryb wpisywania poleceń. Polecenia te pozwalają poruszać się po edytorze - np. wykonać operację kopiuj/wklej, przejść na koniec pliku itp.

Po wydaniu jednoliterowego polecenia `i` Vim przejdzie do trybu `INSERT` (`WPROWADZANIE`) - ogólnie mówiąc, jest to tryb, w którym możemy zmieniać otwarty plik. Status informujący o aktywacji tego trybu znajdziemy w lewym dolnym rogu. By powrócić do trybu `NORMAL` naciskamy klawisz `ESC`.

.. figure:: /images/artykuly/linux//vim-insert.png

            Vim w trybie `INSERT`.

Vim może pracować również w trybie `VISUAL` (`WIZUALNY`). W trybie tym możemy zaznaczyć tekst i wykonać na nim żądane polecenie (np. wytnij). Po wykonaniu polecenia Vim automatycznie zmieni tryb na `NORMAL`. Klawisza `ESC` używamy, by opuścić tryb bez wprowadzania zmian.

.. figure:: /images/artykuly/linux//vim-visual.png

            Vim w trybie `VISUAL`.

Oto lista trybów, z których często korzystam:

+------------+------------------+----------------------------+
| Polecenie  | Tryb             | Opis                       |
+============+==================+============================+
| `i`        | wprowadzanie     | modyfikowanie tekstu       |
+------------+------------------+----------------------------+
| `v`        | wizualny         | zaznaczanie tekstu         |
+------------+------------------+----------------------------+
| `CTRL + v` | wizualny blokowy | zaznaczanie tekstu blokami |
+------------+------------------+----------------------------+
| `V`        | wizualny liniowy | zaznaczanie tekstu liniami |
+------------+------------------+----------------------------+

Oprócz trybów warto znać kilka innych poleceń. Podobnie jak wyżej, przedstawione subiektywnie (dwukropek oznacza przejście do linii poleceń):

+-----------------------+----------------------------------------------------------+
| Polecenie             | Opis                                                     |
+=======================+==========================================================+
| `dd`                  | wytnij linię (delete)                                    |
+-----------------------+----------------------------------------------------------+
| `dw`                  | wytnij słowo (delete)                                    |
+-----------------------+----------------------------------------------------------+
| `yy`                  | kopiuj linię (yank)                                      |
+-----------------------+----------------------------------------------------------+
| `yw`                  | kopiuj słowo (yank)                                      |
+-----------------------+----------------------------------------------------------+
| `P`                   | wklej powyżej/przed kursorem                             |
+-----------------------+----------------------------------------------------------+
| `p`                   | wklej poniżej/za kursorem                                |
+-----------------------+----------------------------------------------------------+
| `/`                   | przeszukaj zawartość bufora                              |
+-----------------------+----------------------------------------------------------+
| `u`                   | cofnij                                                   |
+-----------------------+----------------------------------------------------------+
| `CTRL + r`            | ponów                                                    |
+-----------------------+----------------------------------------------------------+
| `:e <nazwa>`          | otwarcie pliku                                           |
+-----------------------+----------------------------------------------------------+
| `:w`                  | zapis bufora                                             |
+-----------------------+----------------------------------------------------------+
| `:w <nazwa>`          | zapis bufora do pliku o wybranej nazwie                  |
+-----------------------+----------------------------------------------------------+
| `:ls`                 | lista otwartych buforów                                  |
+-----------------------+----------------------------------------------------------+
| `:b <numer>`          | przejdź do bufora                                        |
+-----------------------+----------------------------------------------------------+
| `:bd`                 | zamknięcie bufora                                        |
+-----------------------+----------------------------------------------------------+
| `:split`              | podziel okno poziomo                                     |
+-----------------------+----------------------------------------------------------+
| `:split <nazwa>`      | podziel okno poziomo i otwórz plik                       |
+-----------------------+----------------------------------------------------------+
| `:vsplit`             | podziel okno pionowo                                     |
+-----------------------+----------------------------------------------------------+
| `:vsplit <nazwa>`     | podziel okno pionowo i otwórz plik                       |
+-----------------------+----------------------------------------------------------+
| `:q`                  | zamknięcie okna                                          |
+-----------------------+----------------------------------------------------------+
| `CTRL + w <strzałka>` | przejście do okna po lewej/prawej stronie, na górze/dole |
+-----------------------+----------------------------------------------------------+
| `:! <polecenie>`      | wykonanie polecenia powłoki                              |
+-----------------------+----------------------------------------------------------+

Zapewne niektórzy zwrócili uwagę na słowo *delete* przy słowie *wytnij* oraz *yank* przy *kopiuj*. Wynika to z faktu, że w Vimie właśnie tak te operacje się nazywają. Pewne rozważania na ten temat można znaleźć na `StackExchange <https://ell.stackexchange.com/questions/14632/why-does-yank-in-vim-mean-copy>`__.

Polecenia można ze sobą łączyć. Poniższe zapisze bufor do pliku, a następnie zamknie otwarte okno::

  :wq

Oczywiście powyższa lista nie jest kompletna, Vim oferuje dużo więcej poleceń. Oto kilka stron, na których możesz o nich przeczytać:

* `VIM Editor Commands <http://www.radford.edu/~mhtay/CPSC120/VIM_Editor_Commands.htm>`__
* `vim tips and tricks <https://www.cs.oberlin.edu/~kuperman/help/vim/home.html>`__
* `(youtube) VIM - Split Screen and Navigation - Linux - Shell - BASH <https://www.youtube.com/watch?v=sHGiC6Fp800>`__


Dystrybucje
-----------

Vim może być czymś więcej, niż tylko zwykłym edytorem tekstu - może być środowiskiem programistycznym. W tym celu należy skonfigurować Vima (plik `~/.vimrc`) do naszych potrzeb, zainstalować odpowiednie dodatki i je skonfigurować albo... wykorzystać konfigurację utworzoną przez innych - tak zwaną dystrybucję. Oczywiście dystrybucja taka jest odpowiednio przygotowana, by jej użytkownicy mogli ją dostosowywać.

Chyba najpopularniejszą dystrybucją jest `spf13-vim <http://vim.spf13.com/>`__. Na jej stronie internetowej znajdziemy opis instalacji i dokumentację. Inną dystrybucją jest `space-vim <http://vim.liuchengxu.org/>`__ i to właśnie jej poświęcę uwagę.

Instalacja space-vim
^^^^^^^^^^^^^^^^^^^^

.. attention::
   Polecenia konsoli, pokazane w dalszej części artykułu, przygotowane zostały z myślą o użytkownikach systemu Linux. W przypadku innych systemów operacyjnych polecenia te mogą się różnić.

Instalacja została opisana na stronie internetowej dystrybucji - http://vim.liuchengxu.org/.

Przed przystąpieniem do instalacji musimy upewnić się, że mamy zainstalowany program `git` oraz edytor `vim` z obsługą języka Python.

Poniższe polecenia Vim pomogą sprawdzić, czy Python jest obsługiwany::

  :echo has('python')
  :echo has('python3')

Jeśli którekolwiek z nich wyświetli `1` to znaczy, że nasz Vim posiada wsparcie dla języka Python.

Instalację przeprowadzamy z konta użytkownika, który ma tej dystrybucji używać, poprzez wydanie polecenia::

  bash -c "$(curl -fsSL https://raw.githubusercontent.com/liuchengxu/space-vim/master/install.sh)"

.. figure:: /images/artykuly/linux//vim-space-vim-instalacja.png

            Proces instalacji dystrybucji space-vim.

Po krótkiej chwili możemy uruchomić edytor. Z pewnością zauważymy, że teraz wygląda on zupełnie inaczej.

.. figure:: /images/artykuly/linux//vim-space-vim-konsola.png

            space-vim uruchomiony w oknie konsoli.

.. figure:: /images/artykuly/linux//vim-space-vim-gtk.png

            space-vim uruchomiony z wykorzystaniem graficznego interfejsu.

Konfiguracja
^^^^^^^^^^^^

Instalacja dystrybucji tylko z uwagi na jej wygląd nie jest niczym szczególnym, ważne są dodatki. Otwórzmy zatem plik konfiguracyjny i dostosujmy dystrybucję do naszych potrzeb. Oczywiście całą operację wykonamy za pomocą Vima.

1. Otwieramy plik konfiguracyjny `~/.spacevim` (domyślny plik konfiguracyjny to `~/.vimrc`, jednak na potrzeby dystrybucji został on zmieniony). Będąc w trybie `NORMAL` wykonujemy polecenie::

     :e ~/.spacevim

   Naszym oczom ukaże się taki plik konfiguracyjny::


     " You can enable the existing layers in space-vim and
     " exclude the partial plugins in a certain layer.
     " The command Layer is vaild in the function Layers().
     " Use exclude option if you don't want the full Layer,
     " e.g., Layer 'better-defaults', { 'exclude': 'itchyny/vim-cursorword' }
     function! Layers()

       " Default layers, recommended!
       Layer 'fzf'
       Layer 'unite'
       Layer 'better-defaults'

     endfunction

     " Put your private plugins here.
     function! UserInit()

       " Space has been set as the default leader key,
       " if you want to change it, uncomment and set it here.
       " let g:spacevim_leader = "<\Space>"
       " let g:spacevim_localleader = ','

       " Install private plugins
       " Plug 'extr0py/oni'

     endfunction

     " Put your costom configurations here, e.g., change the colorscheme.
     function! UserConfig()

       " If you enable airline layer and have installed the powerline fonts, set it here.
       " let g:airline_powerline_fonts=1
       " color desert

     endfunction

   Plik ten możemy podzielić na trzy części według widocznych funkcji - warstwy, dodatki użytkownika oraz konfigurację użytkownika.

   **Warstwa** (Layer) to zbiór dodatków - np. warstwa `python` zawiera dodatki pozwalające na pracę ze skryptami języka Python.

   **Dodatki użytkownika** to poszczególne dodatki dla Vima, które chcemy włączyć.

   **Konfiguracja użytkownika** umożliwia zmianę poszczególnych opcji Vima - np. używanego schematu kolorów.

2. Zobaczmy jakie warstwy oferuje nam `space-vim`::

     > ls ~/.space-vim/layers/
     +checkers    +distributions  generate_layers.py  LAYERS.md  +programming  +tools            +vim
     +completion  +fun            +lang               +misc      +themes       +version-control

   Po sprawdzeniu katalogu dystrybucji widać, że zostały one podzielone ze względu na ich role. Jako programista jestem zainteresowany językami C, C++ oraz Python::

     > ls  ~/.space-vim/layers/+lang/
     c-c++   elm     go        html  javascript  markdown  scala       vue
     elixir  erlang  graphviz  java  latex       python    typescript

   Sprawdźmy jakie dodatki zostaną zainstalowane z warstwą `python`::

     > cat  ~/.space-vim/layers/+lang/python/packages.vim
     MP 'tmhedberg/SimpylFold',    { 'for': 'python' }
     MP 'python-mode/python-mode', { 'for': 'python' }


   Proponuję rozejrzeć się chwilę po dostępnych warstwach.

3. W celu włączenia nowych warstw musimy wyedytować funkcję `Layers`. W moim przypadku włączone zostały warstwy: `c-c++`, `python` oraz `git`::

     function! Layers()

       " Default layers, recommended!
       Layer 'fzf'
       Layer 'unite'
       Layer 'better-defaults'

       Layer 'c-c++'
       Layer 'python'

       Layer 'git'

     endfunction

   Po zmianie funkcji `Layers` należy ponownie uruchomić edytor, aby nowe dodatki zostały zainstalowane.

4. Wiele osób narzeka na konieczność używania dziwnych poleceń w Vimie. Zainstalujmy dodatek `novim-mode`, który doda obsługę *klasycznych* skrótów klawiszowych (ich dokumentacja znajduje się `tutaj <https://github.com/tombh/novim-mode>`__).

   W tym celu należy wyedytować funkcję `UserInit`::

     function! UserInit()

       " Space has been set as the default leader key,
       " if you want to change it, uncomment and set it here.
       " let g:spacevim_leader = "<\Space>"
       " let g:spacevim_localleader = ','

       " Install private plugins
       " Plug 'extr0py/oni'

       Plug 'tombh/novim-mode'

     endfunction

   Oczywiście po tej zmianie ponownie uruchamiamy edytor i cieszymy się standardowymi skrótami klawiszowymi. Jestem dość sceptycznie nastawiony do tego dodatku, ale może komuś przypadnie do gustu. Przedstawiam go bardziej jako ciekawostkę.

   Jedna ważna uwaga: `ALT + ;` oraz `ALT + c` sprawi, że otworzy się wiersz poleceń Vim. Ten skrót może się przydać, gdy wpadniemy w tarapaty.

5. Na koniec możemy zmienić konfigurację Vima. Ustawmy inny schemat kolorów oraz *pożyczmy* od `spf13-vim` konfigurację odpowiedzialną za utworzenie aliasów do typowych błędów w poleceniach::

     " Put your costom configurations here, e.g., change the colorscheme.
     function! UserConfig()

       " If you enable airline layer and have installed the powerline fonts, set it here.
       " let g:airline_powerline_fonts=1
       color desert

       " Fix common typos like :W, :Q, etc
       command! -bang -nargs=* -complete=file E e<bang> <args>
       command! -bang -nargs=* -complete=file W w<bang> <args>
       command! -bang -nargs=* -complete=file Wq wq<bang> <args>
       command! -bang -nargs=* -complete=file WQ wq<bang> <args>
       command! -bang Wa wa<bang>
       command! -bang WA wa<bang>
       command! -bang Q q<bang>
       command! -bang QA qa<bang>
       command! -bang Qa qa<bang>

     endfunction

