# Opis projektu

## Wstęp

Celem projektu jest zaimplementowanie systemu rekomendacji filmów.  Na wejściu użytkownik podaje film, który mu się podobał, a system zwraca listę filmów, które również mogą się podobać użytkownikowi.

## Technologie

System został zaimplementowany jako aplikacja webowa przy użyciu Pythonowego frameworku Django. Użyta baza danych to neo4j. Do dostępu do bazy danych z poziomu pythona została użyta oficjalna biblioteka pythonowa neo4j. Pozostałe użyte biblioteki to Pandas, Numpy oraz scikit-learn.

# Instrukcja instalacji

## Instalacja i konfiguracja neo4j

Zainstalować neo4j community edition 5.3.0 według instruckji na stronie https://neo4j.com/docs/operations-manual/current/installation/linux/debian/ .

Umieścić pliki ml-latest-small/movies.csv ml-latest-small/ratings.csv w folderze neo4j-home/import , prawdopodobnie będzie to folder /var/lib/neo4j/import .

Uruchomić usługę neo4j:

    systemctl start neo4j

Uruchomić cypher-shell:

    cypher-shell

Wpisać domyślne dane logowania:
login: neo4j
hasło: neo4j
oraz zgodnie z poleceniami ustawić nowe hasło. Wyjść z cypher-shell.
Załadować dane do bazy komendą:

    cypher-shell -f create_db.cql


## Konfiguracja środowiska python

Wymagania: Linux, python 3.10 lub wyżej, pip, venv

Kod źródłowy projektu umieścić w nowym folderze. Utworzyć wirtualne środowisko:

    python3 -m venv env

Uruchomić wirtualne środowisko:

    source env/bin/activate

Zainstalować zależności:

    pip install -r requirements.txt

W pliku n4jtest/n4jtest/settings.py w linijce 85 wpisać nowo ustawione hasło do neo4j.

## Uruchomienie projektu

Aktywować wirtualne środowisko, uruchomić serwer komendą:

    python3 n4jtest/manage.py runserver

oraz przejść na adres http://127.0.0.1:8000/movie_recs/
