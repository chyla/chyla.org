Swatch - Simple (Log) WATCHer
=============================

**Swatch** („Simple WATCHer”) to skrypt służący do automatycznego monitorowania plików logów oraz automatycznego wykonywania określonych czynności, gdy zostanie wykryty w logach rekord pasujący do zdefiniowanego wcześniej przez użytkownika wzoru (Bauer, 2005, s.447). ”Swatch minimalizuje, ale nie eliminuje potrzeby samodzielnego przeglądania plików dzienników” (Bauer, 2005, s.437). Akcje możliwe do wykonania, podczas wykrycia rekordu pasującego do wzorca, to (Lockhart, 2007, s.268):

* wypisanie komunikatu na konsolę
* wykonanie polecenia
* wysłanie wiadomości e-mail na podane adresy

Każda z powyższych akcji jest w pełni konfigurowalna przez użytkownika, dzięki czemu uzyskano wysoce konfigurowalne narzędzie mogące poinformować użytkownika o zaistniałej sytuacji na wiele różnych sposobów. Konfiguracji wzorców oraz powiadomień należy dokonać z należytą starannością, w taki sposób, aby raportowanie nie było uciążliwe dla użytkownika. W przypadku zbyt szczegółowej konfiguracji oprogramowanie może alarmować użytkownika o rutynowych działaniach wykonywanych w systemie, co może powodować dużą liczbę nieistotnych powiadomień. W przypadku zbyt ogólnej konfiguracji oprogramowanie może nie powiadamiać użytkownika o zaistniałych zagrożeniach (Bauer, 2005, s.446).

Alternatywą dla Swatch jest program **Logsurfer**. W porównaniu do Swatch ma możliwość analizowania kilku wierszy jednocześnie. Pozwala to na tworzenie reguł bazujących na więcej niż jednym rekordzie. W przeciwieństwie do Swatch, który został napisany w języku Perl, Logsurfer napisano w języku C, co może przekładać się na zwiększoną wydajność w porównaniu do konkurenta (Bauer, 2005, s.447).


Literatura
----------

1. Bauer, M. D. (2005). Linux. Serwery. Bezpieczeństwo. Gliwice: Helion.
2. Lockhart, A. (2007). 125 sposobów na bezpieczeństwo sieci. Gliwice: Helion.
3. `Simple Log Watcher <https://sourceforge.net/projects/swatch/>`__
4. `LogSurfer Software and Resources <http://www.crypt.gen.nz/logsurfer/>`__
