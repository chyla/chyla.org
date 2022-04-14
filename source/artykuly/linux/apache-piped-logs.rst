Apache Piped Logs
=================

W Apache dostępna jest opcja "Piped Logs", która umożliwia przesyłanie logów do innego programu za pomocą potoków. Program docelowy jest uruchamiany, a na jego standardowe wejście zapisywane są logi.

Wykorzystanie potoków można skonfigurować za pomocą dyrektywy CustomLog. Zamiast podawać w niej ścieżkę do pliku, w którym mają zostać zapisane logi, podajemy ścieżkę do programu poprzedzoną znakiem ``|`` lub ``|$``.

Przykład::

    CustomLog "|$/bin/patlms-apache-helper --socket /var/run/patlms-apache.sock --logfile /var/log/patlms/apache-helper.log " apache_module

Sam znak ``|`` powoduje uruchomienie podanej aplikacji przez Apache, natomiast ``|$`` uruchomienie aplikacji poprzez shella uruchomionego przez Apache.

Z dokumentacji: *One important use of piped logs is to allow log rotation without having to restart the server. The Apache HTTP Server includes a simple program called rotatelogs for this purpose.*


Literatura
----------

1. `Apache - Log Files <https://httpd.apache.org/docs/2.4/logs.html>`__
