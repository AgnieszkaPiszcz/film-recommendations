# Opis projektu

## Wstęp

Celem projektu jest zaimplementowanie systemu rekomendacji filmów.  Na wejściu użytkownik podaje film, który mu się podobał, a system zwraca listę filmów, które również mogą się podobać użytkownikowi.

## Technologie

System został zaimplementowany jako aplikacja webowa przy użyciu Pythonowego frameworku Django. Użyta baza danych to neo4j. Do dostępu do bazy danych z poziomu pythona została użyta oficjalna biblioteka pythonowa neo4j. Pozostałe użyte biblioteki to Pandas, Numpy oraz scikit-learn.

## Opis działania

opis algorytmu i screenshoty z działania, diagram komunikacji 

Klasa N4jConnection realizuje połączenie do bazy danych. Oferuje metodę query(), która wykonuje zapytanie do bazy danych i zwraca wyniki w formie pandas.DataFrame. 

Za logikę systemu odpowiedzialny jest moduł repository. Opis funkcji:

##### clean_title(title)

Funkcja pomocnicza usuwająca z tytułu filmu znaki specjalne.

##### get_movies()

Funkcja zwraca id filmu, tytuł filmu, wyczyszczony tytuł filmu w formie pandas.DataFrame 

##### get_ratings()

Funkcja zwraca id użytkownika, ocenę filmu, id filmu w formie pandas.DataFrame 

##### search(movies, title)

Funkcja przyjmuje wartość funkcji get_movies() oraz szukaną frazę i zwraca id filmu z tytulem najbardziej podobnym do podanej szukanej frazy. Wyszukiwanie oparte jest o TFIDF.

##### find_similar_movies(title)

Funkcja przyjmuje tytuł filmu wpisany przez użytkownika i zwraca 10 polecanych filmów. Działanie algorytmu polecania:  
1. Znaleźć podobnych użytkowników, czyli wszystkich użytkowników, którym też podobał się podany film.
2. Znaleźć inne filmy, które podobają się użtkownikom podobnym.
3. Obliczyć, ilu prcentom użtkowników podobnych podobał się każdy film z pkt. 2. i znaleźć dobre filmy, czyli filmy, które podobają się co najmniej 10% żytkowników podobnych.
5. Dla każdego filmu z dobrych filmów obliczyć ilu procentom wszystkich użytkowników podobał się dany film.
6. Filmy polecane będą filmami, które podobają się największemu ułamkowi użytkowników podobnych i najmniejszemu ułamkowi wszystkich użytkowników. Dla każdego filmu obliczyć stosunek procenta użytkowników podobnych do procenta wszystkich użytkowników, którym podobał się film. Zwrócić filmy z najwyższym stosunkiem.

## Przykład działania

![screenshot](https://user-images.githubusercontent.com/77401555/214387137-cb457671-13db-4452-b510-183d7e551aea.png "screenshot")
![screenshot](https://user-images.githubusercontent.com/77401555/214387199-b5180803-f8c2-4263-badd-cd64b6859f93.png "screenshot")
![screenshot](https://user-images.githubusercontent.com/77401555/214387224-74c0cf47-98fc-4463-8feb-fdbf1949b18e.png "screenshot")
![screenshot](https://user-images.githubusercontent.com/77401555/214387219-5b92dbdd-f736-41af-86d7-be4e23eacfbe.png "screenshot")


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
