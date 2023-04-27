EduVM 23.04 - Przygotowanie VM
==============================


1. Konfiguacja maszyny wirtualnej:

   * Nazwa: EduVM 23.04 Beta
   * Wersja: Ubuntu (64bit)
   * Skip Unattended Installation
   * RAM: 2048 MB
   * Processors: 2
   * Hard disk size: 30 GB
   * Hard disk format: VDI
   * Współdzielony schowek: Dwukierunkowy
   * Pamięć wideo: 32 MB
   * Kontroler: SATA: Użyj buforowania wejścia/wyjścia gospodarza: Tak
   * Sieć:

     * Karta 1: NAT
     * Karta 2: Karta sieci izolowanej (host-only) - wyłącznie do automatycznej konfiguracji z Ansible


2. Instalacja systemu:

   * Xubuntu ISO: `xubuntu-23.04-minimal-amd64.iso <http://ftp.uni-kl.de/pub/linux/ubuntu-dvd/xubuntu/releases/23.04/release/xubuntu-23.04-minimal-amd64.iso>`__
   * Keyboard: English (US)
   * No updates while installing
   * TZ: Warsaw
   * Name: EduVM
   * Computer's name: EduVM
   * Username: eduvm
   * Password: eduvm
   * Log in automatically


3. Konfiguracja systemu

   Na konfigurowanej maszynie:

   * Ustawienie NOPASSWD dla grupy sudo
   * Zainstalowany openssh-server

   Na sąsiedniej maszynie:

   * Wymiana kluczy z konfigurowanym systemem: ``ssh-copy-id eduvm@192.168.X.X``
   * Uruchomienie konfiguracji, repo tag: https://github.com/chyla/eduvm-preparation/tree/eduvm-2304

   Po zakończonej konfiguracji z Ansible, na konfigurowanej maszynie:

   * Ponowne uruchomienie konfigurowanej maszyny
   * Usunięcie starych pakietów: ``sudo apt purge -y $(dpkg -l | grep -e linux-image -e linux-modules | grep -v $(uname -r) | awk "{print $2}")``
   * Ustawienie ikony menu głównego
   * Przesunięcie panelu z góry na dół
   * Usunięcie historii bash użytkownika: ``rm /home/eduvm/.bash_history``
   * Usunięcie historii bash roota: ``sudo rm /root/.bash_history``
   * Usunięcie zapisanych kluczy: ``rm ~/.ssh/authorized_keys``
   * Wyzerowanie pustego miejsca: ``sudo dd if=/dev/zero of=/root/zero || sudo rm /root/zero``


4. Eksport przygotowanej maszyny

   * Wyłączenie karty sieciowej - host-only
   * Eksport do OCI

     * Polityka adresów MAC: Usuń wszystkie adresy MAC kart sieciowych
