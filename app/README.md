# System Zarządzania Księgowością

Prosty system zarządzania fakturami, klientami, transakcjami i użytkownikami oparty na bazie danych Riak.

## Wymagania

- Python 3.8+
- Tkinter
- Riak DB (uruchomione w kontenerze Docker lub lokalnie)

## Instalacja

1. Sklonuj repozytorium:
```bash
git clone <url-repozytorium>
cd NBD_projekt
```

2. Utwórz i aktywuj wirtualne środowisko:
```bash
python -m venv .venv
# Dla Windows:
.venv\Scripts\activate
# Dla Linux/Mac:
source .venv/bin/activate
```

3. Zainstaluj zależności:
```bash
pip install requests
```

4. Uruchom Riak DB w kontenerze Docker:
```bash
docker run -d -p 8087:8087 -p 8098:8098 --name riak-database basho/riak-kv
```

## Inicjalizacja danych

Aby zainicjalizować bazę danych przykładowymi danymi, uruchom:

```bash
python -m app.main --init-data
```

## Uruchomienie aplikacji

```bash
python -m app.main
```

## Struktura projektu

```
app/
├── Database/
│   └── database.py      # Klasa dostępu do bazy danych Riak
├── Dialog/
│   ├── customer_dialog.py    # Dialog dodawania/edycji klienta
│   ├── invoice_dialog.py     # Dialog dodawania/edycji faktury
│   ├── transaction_dialog.py # Dialog dodawania/edycji transakcji
│   └── user_dialog.py        # Dialog dodawania/edycji użytkownika
├── UI/
│   └── ui.py            # Główny interfejs użytkownika
├── Data/
│   └── dummy_data.py    # Skrypt generujący przykładowe dane
├── methods/
│   ├── customers_operations.py    # Operacje na klientach
│   ├── invoices_operations.py     # Operacje na fakturach
│   ├── transactions_operations.py # Operacje na transakcjach
│   └── users_operations.py        # Operacje na użytkownikach
├── config.py            # Konfiguracja aplikacji
└── main.py              # Główny plik aplikacji
```

## Funkcjonalności

Aplikacja umożliwia:

1. **Zarządzanie klientami**:
    - Dodawanie, edycję i usuwanie klientów
    - Przeglądanie szczegółów klientów

2. **Zarządzanie fakturami**:
    - Tworzenie faktur dla klientów
    - Dodawanie pozycji do faktury
    - Edycję i usuwanie faktur
    - Przeglądanie szczegółów faktury

3. **Zarządzanie transakcjami**:
    - Rejestrowanie transakcji dla faktur
    - Edycję i usuwanie transakcji
    - Przeglądanie szczegółów transakcji

4. **Zarządzanie użytkownikami**:
    - Dodawanie, edycję i usuwanie użytkowników
    - Przypisywanie ról użytkownikom

## Domyślne dane

Po inicjalizacji danych zostanie utworzonych:
- 3 przykładowych klientów
- 6 przykładowych faktur (2 dla każdego klienta)
- Transakcje dla faktur o statusie "Opłacona"
- 3 użytkowników o różnych rolach:
    - admin (administrator)
    - ksiegowy (księgowy)
    - user (użytkownik)

## Uwagi

- Aplikacja korzysta z Riak DB przez HTTP API (port 8098)
- Hasła użytkowników nie są hashowane (tylko do celów demonstracyjnych)