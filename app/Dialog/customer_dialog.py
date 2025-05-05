# app/Dialog/customer_dialog.py
import uuid
from tkinter import ttk, messagebox
import tkinter as tk
from datetime import datetime

class CustomerDialog:
    """Dialog dodawania/edycji klienta."""

    def __init__(self, parent, title, customer=None):
        self.result = None

        # Tworzenie okna dialogowego
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.geometry("500x450")
        dialog.transient(parent)
        dialog.resizable(False, False)

        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        # Pola formularza
        ttk.Label(frame, text="Dane klienta", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2,
                                                                           sticky="w", pady=(0, 15))

        # ID klienta (ukryte, jeśli nowy klient)
        self.customer_id = tk.StringVar(
            value=customer.get("customer_id", str(uuid.uuid4())) if customer else str(uuid.uuid4()))

        # Podstawowe dane
        ttk.Label(frame, text="Nazwa:").grid(row=1, column=0, sticky="w", pady=5)
        self.name = tk.StringVar(value=customer.get("name", "") if customer else "")
        ttk.Entry(frame, textvariable=self.name, width=40).grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(frame, text="Email:").grid(row=2, column=0, sticky="w", pady=5)
        self.email = tk.StringVar(value=customer.get("email", "") if customer else "")
        ttk.Entry(frame, textvariable=self.email, width=40).grid(row=2, column=1, sticky="ew", pady=5)

        ttk.Label(frame, text="Telefon:").grid(row=3, column=0, sticky="w", pady=5)
        self.phone = tk.StringVar(value=customer.get("phone", "") if customer else "")
        ttk.Entry(frame, textvariable=self.phone, width=40).grid(row=3, column=1, sticky="ew", pady=5)

        ttk.Label(frame, text="Adres:").grid(row=4, column=0, sticky="w", pady=5)
        self.address = tk.StringVar(value=customer.get("address", "") if customer else "")
        ttk.Entry(frame, textvariable=self.address, width=40).grid(row=4, column=1, sticky="ew", pady=5)

        ttk.Label(frame, text="Miasto:").grid(row=5, column=0, sticky="w", pady=5)
        self.city = tk.StringVar(value=customer.get("city", "") if customer else "")
        ttk.Entry(frame, textvariable=self.city, width=40).grid(row=5, column=1, sticky="ew", pady=5)

        ttk.Label(frame, text="Kod pocztowy:").grid(row=6, column=0, sticky="w", pady=5)
        self.postal_code = tk.StringVar(value=customer.get("postal_code", "") if customer else "")
        ttk.Entry(frame, textvariable=self.postal_code, width=40).grid(row=6, column=1, sticky="ew", pady=5)

        ttk.Label(frame, text="NIP:").grid(row=7, column=0, sticky="w", pady=5)
        self.tax_id = tk.StringVar(value=customer.get("tax_id", "") if customer else "")
        ttk.Entry(frame, textvariable=self.tax_id, width=40).grid(row=7, column=1, sticky="ew", pady=5)

        # Przyciski
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=8, column=0, columnspan=2, sticky="e", pady=(20, 0))

        ttk.Button(button_frame, text="Anuluj", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Zapisz", command=lambda: self.save_customer(dialog)).pack(side=tk.RIGHT)

        # Konfiguracja wagi kolumn
        frame.columnconfigure(1, weight=1)

        # Ustawienie modalności
        dialog.grab_set()
        parent.wait_window(dialog)

    def save_customer(self, dialog):
        """Zapisanie danych klienta."""
        # Walidacja danych
        if not self.name.get().strip():
            messagebox.showerror("Błąd", "Nazwa klienta jest wymagana.")
            return

        # Walidacja emaila
        email = self.email.get().strip()
        import re
        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Błąd", "Nieprawidłowy format adresu email.")
            return

        # Przygotowanie danych klienta
        self.result = {
            "customer_id": self.customer_id.get(),
            "name": self.name.get().strip(),
            "email": self.email.get().strip(),
            "phone": self.phone.get().strip(),
            "address": self.address.get().strip(),
            "city": self.city.get().strip(),
            "postal_code": self.postal_code.get().strip(),
            "tax_id": self.tax_id.get().strip(),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        dialog.destroy()