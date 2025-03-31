from database import connect_to_riak
from ui import start_gui

def main():
    client = connect_to_riak()
    if client:
        print("Aplikacja księgowa działa!")
        start_gui(client)
    else:
        print("Nie udało się uruchomić aplikacji.")

if __name__ == "__main__":
    main()