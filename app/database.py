import requests
import json
from datetime import datetime


class RiakDatabase:
    def __init__(self, host='localhost', port=8098):
        """Inicjalizacja parametrów połączenia z bazą Riak przez HTTP API."""
        self.base_url = f"http://{host}:{port}"

    def create(self, bucket, key, data):
        """Utworzenie nowego rekordu w bazie danych.

        Args:
            bucket: Nazwa bucketu (np. 'invoices', 'customers')
            key: Klucz rekordu (np. 'invoice:12345')
            data: Dane rekordu w formie słownika
        """
        url = f"{self.base_url}/buckets/{bucket}/keys/{key}"
        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.put(url, data=json.dumps(data), headers=headers)
            return response.status_code in (200, 201, 204)
        except requests.RequestException as e:
            print(f"Błąd podczas tworzenia rekordu: {e}")
            return False

    def read(self, bucket, key):
        """Odczytanie rekordu z bazy danych."""
        url = f"{self.base_url}/buckets/{bucket}/keys/{key}"
        headers = {'Accept': 'application/json'}

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return None
            else:
                print(f"Błąd podczas odczytu rekordu: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"Błąd podczas odczytu rekordu: {e}")
            return None

    def update(self, bucket, key, data):
        """Aktualizacja istniejącego rekordu w bazie danych."""
        # W Riak update działa tak samo jak create
        return self.create(bucket, key, data)

    def delete(self, bucket, key):
        """Usunięcie rekordu z bazy danych."""
        url = f"{self.base_url}/buckets/{bucket}/keys/{key}"

        try:
            response = requests.delete(url)
            return response.status_code in (200, 204)
        except requests.RequestException as e:
            print(f"Błąd podczas usuwania rekordu: {e}")
            return False

    def list_keys(self, bucket):
        """Pobranie listy wszystkich kluczy w buckecie."""
        url = f"{self.base_url}/buckets/{bucket}/keys?keys=true"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                try:
                    # Format odpowiedzi: {"keys":["key1","key2",...]}
                    keys_data = response.json()
                    return keys_data.get('keys', [])
                except json.JSONDecodeError:
                    print("Błąd podczas parsowania odpowiedzi JSON")
                    return []
            else:
                print(f"Błąd podczas pobierania kluczy: {response.status_code}")
                return []
        except requests.RequestException as e:
            print(f"Błąd podczas pobierania kluczy: {e}")
            return []