import tkinter as tk
from tkinter import ttk, messagebox
import uuid
from datetime import datetime

class TransactionDialog:
    """dialog dodawania/edycji transakcji."""

    def __init__(self, parent, title, db, transaction=None):
        self.result = None
        self.db = db

        # Tworzenie okna dialogowego
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.geometry("500x400")
        dialog.transient(parent)
        dialog.resizable(False, False)

        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        # Pola formularza
        ttk.Label(frame, text="Dane transakcji", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2,
                                                                              sticky="w", pady=(0, 15))

        # ID transakcji
        self.transaction_id = tk.StringVar(
            value=transaction.get("transaction_id", str(uuid.uuid4())) if transaction else str(uuid.uuid4()))

        # Faktura
        ttk.Label(frame, text="Faktura:").grid(row=1, column=0, sticky="w", pady=5)
        self.invoice_id = tk.StringVar(value=transaction.get("invoice_id", "") if transaction else "")

        # Lista faktur
        invoice_frame = ttk.Frame(frame)
        invoice_frame.grid(row=1, column=1, sticky="ew", pady=5)

        invoices = []
        invoice_keys = db.list_keys("invoices")
        for key in invoice_keys:
            invoice = db.read("invoices", key)
            if invoice:
                invoice_id = key.replace("invoice:", "")
                customer_id = invoice.get("customer_id", "")
                customer_name = "Nieznany"

                if customer_id:
                    customer = db.read("customers", f"customer:{customer_id}")
                    if customer:
                        customer_name = customer.get("name", "Nieznany")

                amount = invoice.get("amount", 0)
                currency = invoice.get("currency", "PLN")
                invoices.append((invoice_id, f"{customer_name} - {amount} {currency}"))

        invoice_items = [f"{id} - {desc}" for id, desc in invoices]
        self.invoice_combobox = ttk.Combobox(invoice_frame, values=invoice_items, width=40)
        self.invoice_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Wybór faktury jeśli edytujemy transakcję
        if transaction and transaction.get("invoice_id"):
            for idx, (iid, _) in enumerate(invoices):
                if iid == transaction.get("invoice_id"):
                    self.invoice_combobox.current(idx)
                    break

        # data transakcji
        ttk.Label(frame, text="data transakcji:").grid(row=2, column=0, sticky="w", pady=5)
        self.transaction_date = tk.StringVar(
            value=transaction.get("transaction_date",
                                  datetime.now().strftime("%Y-%m-%d")) if transaction else datetime.now().strftime(
                "%Y-%m-%d"))
        ttk.Entry(frame, textvariable=self.transaction_date, width=40).grid(row=2, column=1, sticky="ew", pady=5)

        # Kwota
        ttk.Label(frame, text="Kwota:").grid(row=3, column=0, sticky="w", pady=5)
        self.amount = tk.StringVar(value=transaction.get("amount", "0.00") if transaction else "0.00")
        ttk.Entry(frame, textvariable=self.amount, width=40).grid(row=3, column=1, sticky="ew", pady=5)

        # Metoda płatności
        ttk.Label(frame, text="Metoda płatności:").grid(row=4, column=0, sticky="w", pady=5)
        self.payment_method = tk.StringVar(
            value=transaction.get("payment_method", "Przelew") if transaction else "Przelew")
        methods = ["Przelew", "Gotówka", "Karta", "BLIK", "Inne"]
        ttk.Combobox(frame, textvariable=self.payment_method, values=methods, state="readonly", width=20).grid(row=4,
                                                                                                               column=1,
                                                                                                               sticky="w",
                                                                                                               pady=5)

        # Status
        ttk.Label(frame, text="Status:").grid(row=5, column=0, sticky="w", pady=5)
        self.status = tk.StringVar(value=transaction.get("status", "Zakończona") if transaction else "Zakończona")
        statuses = ["Zakończona", "W trakcie", "Anulowana", "Błąd"]
        ttk.Combobox(frame, textvariable=self.status, values=statuses, state="readonly", width=20).grid(row=5, column=1,
                                                                                                        sticky="w",
                                                                                                        pady=5)

        # Numer referencyjny
        ttk.Label(frame, text="Nr referencyjny:").grid(row=6, column=0, sticky="w", pady=5)
        self.reference_number = tk.StringVar(value=transaction.get("reference_number", "") if transaction else "")
        ttk.Entry(frame, textvariable=self.reference_number, width=40).grid(row=6, column=1, sticky="ew", pady=5)

        # Przyciski
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=7, column=0, columnspan=2, sticky="e", pady=(20, 0))

        ttk.Button(button_frame, text="Anuluj", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Zapisz", command=lambda: self.save_transaction(dialog)).pack(side=tk.RIGHT)

        # Konfiguracja wagi kolumn
        frame.columnconfigure(1, weight=1)

        # Ustawienie modalności
        dialog.grab_set()
        parent.wait_window(dialog)

    def save_transaction(self, dialog):
        """Zapisanie danych transakcji."""
        # Walidacja danych
        if not self.invoice_combobox.get():
            messagebox.showerror("Błąd", "Wybierz fakturę.")
            return

        try:
            if self.transaction_date.get():
                datetime.strptime(self.transaction_date.get(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Błąd", "Nieprawidłowy format daty transakcji (RRRR-MM-DD).")
            return

        try:
            amount = float(self.amount.get())
            if amount <= 0:
                messagebox.showerror("Błąd", "Kwota transakcji musi być większa od zera.")
                return
        except ValueError:
            messagebox.showerror("Błąd", "Nieprawidłowa wartość kwoty transakcji.")
            return

        # Pobranie ID faktury z comboboxa
        invoice_id = self.invoice_combobox.get().split(" - ")[0] if self.invoice_combobox.get() else ""

        # Przygotowanie danych transakcji
        self.result = {
            "transaction_id": self.transaction_id.get(),
            "invoice_id": invoice_id,
            "transaction_date": self.transaction_date.get(),
            "amount": float(self.amount.get()),
            "payment_method": self.payment_method.get(),
            "status": self.status.get(),
            "reference_number": self.reference_number.get(),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        dialog.destroy()