EduVM 25.10 - Przygotowanie VM
==============================


1. Konfiguacja maszyny wirtualnej:

   * Nazwa: EduVM 25.10
   * Wersja: Ubuntu (64bit)
   * Skip Unattended Installation
   * RAM: 2048 MB
   * Processors: 4
   * Hard disk size: 40 GB
   * Hard disk format: VDI
   * Współdzielony schowek: Dwukierunkowy
   * Pamięć wideo: 32 MB
   * Kontroler: SATA: Użyj buforowania wejścia/wyjścia gospodarza: Tak
   * Sieć:

     * Karta 1: NAT
     * Karta 2: Karta sieci izolowanej (host-only) - wyłącznie do automatycznej konfiguracji z Ansible


2. Instalacja systemu:

   * Xubuntu ISO: `xubuntu-25.10-minimal-amd64.iso <https://torrent.ubuntu.com/xubuntu/releases/questing/release/minimal/xubuntu-25.10-minimal-amd64.iso.torrent>`__
   * Keyboard: English (US)
   * No updates while installing
   * TZ: Warsaw
   * Name: EduVM
   * Computer's name: EduVM
   * Username: eduvm
   * Password: eduvm


3. Konfiguracja systemu

   Na konfigurowanej maszynie:

   * Ustawienie NOPASSWD dla grupy sudo
   * Zainstalowany openssh-server

   Na sąsiedniej maszynie:

   * Wymiana kluczy z konfigurowanym systemem: ``ssh-copy-id eduvm@192.168.X.X``
   * Uruchomienie konfiguracji, repo tag: https://github.com/chyla/eduvm-preparation/tree/eduvm-2510

   Po zakończonej konfiguracji z Ansible, na konfigurowanej maszynie:

   * Ponowne uruchomienie konfigurowanej maszyny
   * Usunięcie starych pakietów: ``sudo apt purge -y $(dpkg -l | grep -e linux-image -e linux-modules | grep -v $(uname -r) | awk '{print $2}')``
   * Usunięcie SSH: ``sudo apt purge -y openssh-server openssh-sftp-server``
   * Przesunięcie panelu z góry na dół
   * Usunięcie historii bash użytkownika: ``rm /home/eduvm/.bash_history``
   * Usunięcie historii bash roota: ``sudo rm /root/.bash_history``
   * Usunięcie zapisanych kluczy: ``rm -rf ~/.ssh``
   * Usunięcie bazy kluczy: ``rm ~/.local/share/keyrings/login.keyring``
   * Wyzerowanie pustego miejsca: ``sudo dd if=/dev/zero of=/root/zero || sudo rm /root/zero``


4. Eksport przygotowanej maszyny

   * Wyłączenie karty sieciowej - host-only
   * Eksport

     * Polityka adresów MAC: Usuń wszystkie adresy MAC kart sieciowych
