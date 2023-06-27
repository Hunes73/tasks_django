# Tasks App

# Spis treści

- [Opis aplikacji](#opis-aplikacji)
- [Uruchomienie aplikacji](#uruchomienie-aplikacji)
- [Działanie aplikacji](#działanie-aplikacji)
- [Testy](#testy)
- [Dodatkowe informacje](#dodatkowe-informacje)


# Opis aplikacji

Aplkacja pozwala na wyświetlanie, dodawanie, usuwanie i edycję zadań. Zadania są przechowywane w bazie danych.
Komunikacja z aplikacją odbywa się poprzez REST API. Aplikacja została napisana w języku Python z wykorzystaniem frameworka Django.
# Uruchomienie aplikacji
1. Pobierz repozytorium


2. Przejdź do katalogu z projektem


3. Utórz plik .env i uzupełnij go według przykładowego wzoru:
```bash
SECRET_KEY='c_r-e8v1divj8y+hu@-w=n#$xj#ciuejybd3_(k2h789(mcv8$'
DEBUG=False

## Database Credentials
POSTGRES_DB=tasks
POSTGRES_USER=admin
POSTGRES_PASSWORD=SuperSecretPassword1!
```

4. Zbuduj i uruchom kontenery
```bash
 docker-compose up --build
```

5. Aplikacja jest dostępna pod adresem http://localhost:80

    W przypadku problemów z wyświetleniem strony, należy sprawdzić czy port 80 jest wolny i nie jest używany przez inną aplikację oraz zablokować cache przeglądarki (Chrome: Ctrl + Shift + I -> Network -> Disable cache)



6. Aby zatrzymać kontenery wpisz w konsoli
```bash
 docker-compose down --volume
```

# Działanie aplikacji
Jako, że aplikacja działa jako REST API, do jej obsługi należy użyć narzędzi takich jak Postman, lub używając dostępnego pod adresem http://localhost:80/swagger interfejsu Swagger UI lub dokumentacji ReDoc pod adresem http://localhost:80/redoc.

Aby wykonać jakiekolwiek zapytanie, musimy się jednak  najpierw zalogować. Zrobimy to pod adresem http://localhost:80/api/accounts/login. Na start dostępne są dwa konta użytkowników:
- username: user1, password: password1
- username: user2, password: password2

Możemy też utworzyć kolejne konta, pod adresem http://localhost:80/api/accounts/register.

Po zalogowaniu zostaniemy przeniesieni do witryny, w której wyświetlą się przypisane do naszego użytkownika zadania.
Korzystając z API możemy wykonać następujące operacje:
- wyświetlenie listy wszystkich zadań
- wyświetlenie listy zadań przypisanych do zalogowanego użytkownika
- wyświetlenie szczegółów zadania o podanym id
- dodanie nowego zadania
- edycja zadania o podanym id
- usunięcie zadania o podanym id
- wyświetlenie historii zmian wszystkich zadań
- wyświetlenie historii zmian zadania o podanym id
- wyślenie historii zadania o podanym id w określonym czasie

Aby wylogować się z aplikacji należy wykonać zapytanie pod adresem http://localhost:80/api/accounts/logout.

# Testy
Aby uruchomić testy należy wykonać polecenie
```bash
 docker-compose exec web python manage.py test
```
Niestety nadal mam problemy z jednym z testów, który nie przechodzi, ale zadałem już pytanie na stackoverflow i czekam na odpowiedź.

# Dodatkowe informacje
Zależności użyte w projekcie są aktualne na dzień 27.06.2023.

Aplikacja została napisana w języku Python z wykorzystaniem frameworka Django.

Do komunikacji z bazą danych wykorzystano ORM Django.

Jako bazę danych wykorzystano PostgreSQL.

Do testowania aplikacji wykorzystano bibliotekę pytest.

Do przechowywania historii danych wykorzystano django-simple-history

Do autoryzacji i autentykacji użytkowników wykorzystano wbudowane w Django mechanizmy. 

Do dokumentacji API wykorzystano bibliotekę drf-yasg.

Do uruchomienia aplikacji w kontenerach wykorzystano Docker oraz docker-compose.

Do zarządzania wersjami wykorzystano git.

#### Lista wszystkich użytych bibliotek znajduje się w pliku requirements.txt