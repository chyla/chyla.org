Repozytorium pakietów
=====================

Utworzyłem repozytorium pakietów dla Ubuntu LTS, by dostarczyć kilka programów w nowszych wersjach. Do repozytorium trafiają programy i bilioteki, których używam. W ten sposób wiem czy dany pakiet działa poprawnie i czy jest aktualny. Oznacza to także, że możesz nie znaleźć tu pakietu, który Ciebie interesuje.

Większość pakietów to "backporty" z nowszych wersji Ubuntu albo Debiana, chociaż są też pakiety własne.

Przykładowe pakiety zawarte w repozytorium (w zależności od wydania Ubuntu):

* cppcheck,
* emacs,
* fonts-ibm-plex,
* git,
* universal-ctags,
* wireshark.


Aktualną listę pakietów znajdziesz na stronie launchpad danego repozytorium.


Dodanie repozytorium
--------------------

.. important::

  Pamiętaj, że:

  * dodajesz to repozytorium na własną odpowiedzialność,
  * te pakiety zastępują pakiety systemowe,
  * nie mogę zagwarantować, że któryś z pakietów nie zepsuje Twojego systemu.

Polecam wykorzystać `mechanizm Apt-Pinning <https://wiki.debian.org/AptConfiguration#apt_preferences_.28APT_pinning.29>`__ do wyboru pakietów, które Ciebie interesują.


Ubuntu 22.04
^^^^^^^^^^^^

Jeszcze niedostępne.


Przestarzałe
^^^^^^^^^^^^

**Poniższe repozytoria nie otrzymują już nowszych wersji pakietów.**

Ubuntu 20.04
************

Dodanie repozytorium do systemu sprowadza się do wykonania tych poleceń:

.. code:: bash

    sudo add-apt-repository ppa:extk/chyla.org-repository-for-ubuntu-20.04
    sudo apt-get update

Pełna lista pakietów i dokładny opis instalacji znajduje się na `stronie launchpad.net <https://launchpad.net/~extk/+archive/ubuntu/chyla.org-repository-for-ubuntu-20.04>`__.

Ubuntu 18.04
************

Dodanie repozytorium do systemu sprowadza się do wykonania tych poleceń:

.. code:: bash

    sudo add-apt-repository ppa:extk/chyla.org-repository-for-ubuntu-18.04
    sudo apt-get update

Pełna lista pakietów i dokładny opis instalacji znajduje się na `stronie launchpad.net <https://launchpad.net/~extk/+archive/ubuntu/chyla.org-repository-for-ubuntu-18.04>`__.
