# app/data/dummy_data.py
import uuid
from datetime import datetime, timedelta
from app.Database.database import RiakDatabase

def create_dummy_data(db):
    """
    Tworzy przykładowe dane w bazie Riak.
    
    Args:
        db: Instancja RiakDatabase
    """
    # Sprawdzenie połączenia z bazą danych
    print("Tworzenie przykładowych danych...")

    # Tworzenie przykładowych klientów
    customers = [
        {
            "customer_id": str(uuid.uuid4()),
            "name": "ABC Sp. z o.o.",
            "email": "kontakt@abc.pl",
            "phone": "+48 123 456 789",
            "address": "ul. Przykładowa 1",
            "city": "Warszawa",
            "postal_code": "00-001",
            "tax_id": "1234567890",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "customer_id": str(uuid.uuid4()),
            "name": "XYZ S.A.",
            "email": "biuro@xyz.pl",
            "phone": "+48 987 654 321",
            "address": "ul. Testowa 10",
            "city": "Kraków",
            "postal_code": "30-001",
            "tax_id": "0987654321",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "customer_id": str(uuid.uuid4()),
            "name": "Tech Solutions",
            "email": "info@techsolutions.pl",
            "phone": "+48 111 222 333",
            "address": "ul. Programistów 5",
            "city": "Wrocław",
            "postal_code": "50-001",
            "tax_id": "5555666777",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    ]

    # Zapisanie klientów do bazy
    for customer in customers:
        key = f"customer:{customer['customer_id']}"
        db.create("customers", key, customer)
        print(f"Dodano klienta: {customer['name']}")

    # Tworzenie przykładowych faktur
    invoices = []

    for i, customer in enumerate(customers):
        # Dla każdego klienta tworzymy 2 faktury
        for j in range(2):
            invoice_id = str(uuid.uuid4())
            invoice_date = datetime.now() - timedelta(days=j*15)
            due_date = invoice_date + timedelta(days=14)

            # Pozycje faktury
            items = [
                {
                    "item_id": str(uuid.uuid4())[:8],
                    "description": f"Usługa {j+1}",
                    "quantity": j+1,
                    "unit_price": 100.0 * (j+1)
                },
                {
                    "item_id": str(uuid.uuid4())[:8],
                    "description": f"Produkt {j+1}",
                    "quantity": 2,
                    "unit_price": 50.0 * (j+1)
                }
            ]

            # Obliczanie kwoty faktury
            amount = sum(item["quantity"] * item["unit_price"] for item in items)

            # Status faktury
            status = "Wystawiona" if j == 0 else "Opłacona"

            invoice = {
                "invoice_id": invoice_id,
                "customer_id": customer["customer_id"],
                "date": invoice_date.strftime("%Y-%m-%d"),
                "due_date": due_date.strftime("%Y-%m-%d"),
                "amount": amount,
                "currency": "PLN",
                "status": status,
                "items": items,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            invoices.append(invoice)

            # Zapisanie faktury do bazy
            key = f"invoice:{invoice_id}"
            db.create("invoices", key, invoice)
            print(f"Dodano fakturę dla klienta {customer['name']}: {amount} PLN")

    # Tworzenie przykładowych transakcji dla opłaconych faktur
    for invoice in invoices:
        if invoice["status"] == "Opłacona":
            transaction_id = str(uuid.uuid4())
            transaction_date = datetime.strptime(invoice["date"], "%Y-%m-%d") + timedelta(days=5)

            transaction = {
                "transaction_id": transaction_id,
                "invoice_id": invoice["invoice_id"],
                "transaction_date": transaction_date.strftime("%Y-%m-%d"),
                "amount": invoice["amount"],
                "payment_method": "Przelew",
                "status": "Zakończona",
                "reference_number": f"REF/{transaction_date.year}/{transaction_id[:8]}",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            # Zapisanie transakcji do bazy
            key = f"transaction:{transaction_id}"
            db.create("transactions", key, transaction)
            print(f"Dodano transakcję dla faktury {invoice['invoice_id']}: {transaction['amount']} PLN")

    # Tworzenie przykładowych użytkowników
    users = [
        {
            "user_id": str(uuid.uuid4()),
            "username": "admin",
            "email": "admin@system.pl",
            "password": "admin123",  # W rzeczywistej aplikacji hasło powinno być zahaszowane
            "role": "administrator",
            "is_active": True,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "user_id": str(uuid.uuid4()),
            "username": "ksiegowy",
            "email": "ksiegowy@system.pl",
            "password": "ksiegowy123",
            "role": "księgowy",
            "is_active": True,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "user_id": str(uuid.uuid4()),
            "username": "user",
            "email": "user@system.pl",
            "password": "user123",
            "role": "użytkownik",
            "is_active": True,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    ]

    # Zapisanie użytkowników do bazy
    for user in users:
        key = f"user:{user['user_id']}"
        db.create("users", key, user)
        print(f"Dodano użytkownika: {user['username']}")

    print("Tworzenie przykładowych danych zakończone.")


if __name__ == "__main__":
    # Parametry połączenia z Riak
    db = RiakDatabase(host='localhost', port=8098)
    create_dummy_data(db)