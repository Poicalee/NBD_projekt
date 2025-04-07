import tkinter as tk
import requests
from app.Database.database import RiakDatabase
from app.UI.ui import UserInterface



def test_connection(host, port):
    """Sprawdzenie połączenia z Riak."""
    try:
        response = requests.get(f"http://{host}:{port}/ping")
        if response.status_code == 200 and response.text == "OK":
            print("Połączenie z Riak nawiązane pomyślnie!")
            return True
        else:
            print(f"Błąd podczas testowania połączenia: kod {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"Błąd podczas nawiązywania połączenia z Riak: {e}")
        return False


def main():
    """Główna funkcja uruchamiająca aplikację."""
    # Parametry połączenia z Riak
    host = 'localhost'
    port = 8098  # Port HTTP API Riak

    # Testowanie połączenia
    if not test_connection(host, port):
        print("Nie można nawiązać połączenia z bazą Riak. Sprawdź czy kontener Docker jest uruchomiony.")
        return

    # Inicjalizacja połączenia z bazą danych
    db = RiakDatabase(host=host, port=port)

    # Utworzenie interfejsu użytkownika
    root = tk.Tk()
    app = UserInterface(root, db)

    # Uruchomienie głównej pętli aplikacji
    root.mainloop()


if __name__ == "__main__":
    main()