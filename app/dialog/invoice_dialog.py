import tkinter as tk
from tkinter import ttk, messagebox
import uuid
from datetime import datetime

class InvoiceDialog:
    """dialog dodawania/edycji faktury."""

    def __init__(self, parent, title, db, invoice=None):
        self.result = None
        self.db = db

        # Tworzenie okna dialogowego
        dialog = tk.Toplevel(parent)
        dialog.title(title)
        dialog.geometry("600x600")
        dialog.transient(parent)
        dialog.resizable(False, False)

        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        # Pola formularza
        ttk.Label(frame, text="Dane faktury", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2, sticky="w",
                                                                           pady=(0, 15))

        # ID faktury
        self.invoice_id = tk.StringVar(
            value=invoice.get("invoice_id", str(uuid.uuid4())) if invoice else str(uuid.uuid4()))

        # Klient
        ttk.Label(frame, text="Klient:").grid(row=1, column=0, sticky="w", pady=5)
        self.customer_id = tk.StringVar(value=invoice.get("customer_id", "") if invoice else "")

        # Lista klientów
        customer_frame = ttk.Frame(frame)
        customer_frame.grid(row=1, column=1, sticky="ew", pady=5)

        customers = []
        customer_keys = db.list_keys("customers")
        for key in customer_keys:
            customer = db.read("customers", key)
            if customer:
                customer_id = key.replace("customer:", "")
                customer_name = customer.get("name", "")
                customers.append((customer_id, customer_name))

        customer_names = [f"{id} - {name}" for id, name in customers]
        self.customer_combobox = ttk.Combobox(customer_frame, values=customer_names, width=40)
        self.customer_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Wybór klienta jeśli edytujemy fakturę
        if invoice and invoice.get("customer_id"):
            for idx, (cid, _) in enumerate(customers):
                if cid == invoice.get("customer_id"):
                    self.customer_combobox.current(idx)
                    break

        # data wystawienia
        ttk.Label(frame, text="data wystawienia:").grid(row=2, column=0, sticky="w", pady=5)
        self.date = tk.StringVar(
            value=invoice.get("date", datetime.now().strftime("%Y-%m-%d")) if invoice else datetime.now().strftime(
                "%Y-%m-%d"))
        ttk.Entry(frame, textvariable=self.date, width=40).grid(row=2, column=1, sticky="ew", pady=5)

        # Termin płatności
        ttk.Label(frame, text="Termin płatności:").grid(row=3, column=0, sticky="w", pady=5)
        self.due_date = tk.StringVar(value=invoice.get("due_date", "") if invoice else "")
        ttk.Entry(frame, textvariable=self.due_date, width=40).grid(row=3, column=1, sticky="ew", pady=5)

        # Kwota
        ttk.Label(frame, text="Kwota:").grid(row=4, column=0, sticky="w", pady=5)
        self.amount = tk.StringVar(value=invoice.get("amount", "0.00") if invoice else "0.00")
        ttk.Entry(frame, textvariable=self.amount, width=40).grid(row=4, column=1, sticky="ew", pady=5)

        # Waluta
        ttk.Label(frame, text="Waluta:").grid(row=5, column=0, sticky="w", pady=5)
        self.currency = tk.StringVar(value=invoice.get("currency", "PLN") if invoice else "PLN")
        currencies = ["PLN", "EUR", "USD", "GBP"]
        ttk.Combobox(frame, textvariable=self.currency, values=currencies, state="readonly", width=10).grid(row=5,
                                                                                                            column=1,
                                                                                                            sticky="w",
                                                                                                            pady=5)

        # Status
        ttk.Label(frame, text="Status:").grid(row=6, column=0, sticky="w", pady=5)
        self.status = tk.StringVar(value=invoice.get("status", "Wystawiona") if invoice else "Wystawiona")
        statuses = ["Wystawiona", "Opłacona", "Częściowo opłacona", "Anulowana", "Przeterminowana"]
        ttk.Combobox(frame, textvariable=self.status, values=statuses, state="readonly", width=20).grid(row=6, column=1,
                                                                                                        sticky="w",
                                                                                                        pady=5)

        # Pozycje faktury
        items_frame = ttk.LabelFrame(frame, text="Pozycje faktury")
        items_frame.grid(row=7, column=0, columnspan=2, sticky="nsew", pady=(15, 5))

        # Lista pozycji
        self.items = invoice.get("items", []) if invoice else []

        # Treeview dla pozycji faktury
        columns = ("ID", "Opis", "Ilość", "Cena jedn.", "Wartość")
        self.items_tree = ttk.Treeview(items_frame, columns=columns, height=5)

        self.items_tree.heading("#0", text="")
        self.items_tree.column("#0", width=0, stretch=tk.NO)

        for col in columns:
            self.items_tree.heading(col, text=col)
            self.items_tree.column(col, width=100)

        self.items_tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=5)

        # Przyciski dla pozycji
        items_buttons_frame = ttk.Frame(items_frame)
        items_buttons_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        ttk.Button(items_buttons_frame, text="Dodaj pozycję", command=self.add_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(items_buttons_frame, text="Edytuj pozycję", command=self.edit_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(items_buttons_frame, text="Usuń pozycję", command=self.delete_item).pack(side=tk.LEFT, padx=5)

        # Wypełnienie danych pozycji
        self.refresh_items()

        # Przyciski akcji
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=8, column=0, columnspan=2, sticky="e", pady=(20, 0))

        ttk.Button(button_frame, text="Anuluj", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Zapisz", command=lambda: self.save_invoice(dialog)).pack(side=tk.RIGHT)

        # Konfiguracja wagi wierszy i kolumn
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(7, weight=1)

        # Ustawienie modalności
        dialog.grab_set()
        parent.wait_window(dialog)

    def refresh_items(self):
        """Odświeżenie listy pozycji faktury."""
        # Wyczyszczenie listy
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)

        # Wypełnienie danych pozycji
        for item in self.items:
            value = item.get("quantity", 0) * item.get("unit_price", 0)
            self.items_tree.insert("", tk.END, values=(
                item.get("item_id", ""),
                item.get("description", ""),
                item.get("quantity", 0),
                item.get("unit_price", 0),
                value
            ))

    def add_item(self):
        """Dodanie nowej pozycji do faktury."""
        # Tworzenie nowego ID dla pozycji
        item_id = str(uuid.uuid4())[:8]

        # Okno dialogowe do wprowadzenia danych pozycji
        dialog = tk.Toplevel(self.items_tree.winfo_toplevel())
        dialog.title("Dodaj pozycję faktury")
        dialog.geometry("400x250")
        dialog.transient(self.items_tree.winfo_toplevel())
        dialog.resizable(False, False)

        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        # Pola formularza
        ttk.Label(frame, text="Opis:").grid(row=0, column=0, sticky="w", pady=5)
        description = tk.StringVar()
        ttk.Entry(frame, textvariable=description, width=30).grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(frame, text="Ilość:").grid(row=1, column=0, sticky="w", pady=5)
        quantity = tk.StringVar(value="1")
        ttk.Entry(frame, textvariable=quantity, width=30).grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(frame, text="Cena jednostkowa:").grid(row=2, column=0, sticky="w", pady=5)
        unit_price = tk.StringVar(value="0.00")
        ttk.Entry(frame, textvariable=unit_price, width=30).grid(row=2, column=1, sticky="ew", pady=5)

        # Przyciski
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=2, sticky="e", pady=(20, 0))

        ttk.Button(button_frame, text="Anuluj", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Dodaj", command=lambda: self.save_item(dialog, item_id, description.get(),
                                                                              quantity.get(), unit_price.get())).pack(
            side=tk.RIGHT)

        # Konfiguracja wagi kolumn
        frame.columnconfigure(1, weight=1)

        # Ustawienie modalności
        dialog.grab_set()
        dialog.wait_window()

    def edit_item(self):
        """Edycja istniejącej pozycji faktury."""
        selected = self.items_tree.selection()
        if not selected:
            messagebox.showwarning("Ostrzeżenie", "Wybierz pozycję do edycji")
            return

        # Pobranie danych wybranej pozycji
        item_id = self.items_tree.item(selected[0])["values"][0]

        # Znalezienie pozycji w liście
        selected_item = None
        for item in self.items:
            if item.get("item_id") == item_id:
                selected_item = item
                break

        if not selected_item:
            return

        # Okno dialogowe do edycji danych pozycji
        dialog = tk.Toplevel(self.items_tree.winfo_toplevel())
        dialog.title("Edytuj pozycję faktury")
        dialog.geometry("400x250")
        dialog.transient(self.items_tree.winfo_toplevel())
        dialog.resizable(False, False)

        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        # Pola formularza
        ttk.Label(frame, text="Opis:").grid(row=0, column=0, sticky="w", pady=5)
        description = tk.StringVar(value=selected_item.get("description", ""))
        ttk.Entry(frame, textvariable=description, width=30).grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(frame, text="Ilość:").grid(row=1, column=0, sticky="w", pady=5)
        quantity = tk.StringVar(value=selected_item.get("quantity", 1))
        ttk.Entry(frame, textvariable=quantity, width=30).grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(frame, text="Cena jednostkowa:").grid(row=2, column=0, sticky="w", pady=5)
        unit_price = tk.StringVar(value=selected_item.get("unit_price", 0.00))
        ttk.Entry(frame, textvariable=unit_price, width=30).grid(row=2, column=1, sticky="ew", pady=5)

        # Przyciski
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=2, sticky="e", pady=(20, 0))

        ttk.Button(button_frame, text="Anuluj", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Zapisz", command=lambda: self.save_item(dialog, item_id, description.get(),
                                                                               quantity.get(), unit_price.get(),
                                                                               True)).pack(
            side=tk.RIGHT)

        # Konfiguracja wagi kolumn
        frame.columnconfigure(1, weight=1)

        # Ustawienie modalności
        dialog.grab_set()
        dialog.wait_window()

    def delete_item(self):
        """Usunięcie pozycji faktury."""
        selected = self.items_tree.selection()
        if not selected:
            messagebox.showwarning("Ostrzeżenie", "Wybierz pozycję do usunięcia")
            return

        if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć tę pozycję?"):
            # Pobranie ID wybranej pozycji
            item_id = self.items_tree.item(selected[0])["values"][0]

            # Usunięcie pozycji z listy
            self.items = [item for item in self.items if item.get("item_id") != item_id]

            # Odświeżenie widoku
            self.refresh_items()

    def save_item(self, dialog, item_id, description, quantity, unit_price, is_edit=False):
        """Zapisanie pozycji faktury."""
        # Walidacja danych
        if not description.strip():
            messagebox.showerror("Błąd", "Opis pozycji jest wymagany.")
            return

        try:
            quantity = float(quantity)
            if quantity <= 0:
                messagebox.showerror("Błąd", "Ilość musi być większa od zera.")
                return
        except ValueError:
            messagebox.showerror("Błąd", "Nieprawidłowa wartość ilości.")
            return

        try:
            unit_price = float(unit_price)
            if unit_price < 0:
                messagebox.showerror("Błąd", "Cena jednostkowa nie może być ujemna.")
                return
        except ValueError:
            messagebox.showerror("Błąd", "Nieprawidłowa wartość ceny jednostkowej.")
            return

        # Przygotowanie danych pozycji
        item_data = {
            "item_id": item_id,
            "description": description.strip(),
            "quantity": quantity,
            "unit_price": unit_price
        }

        # Aktualizacja lub dodanie pozycji
        if is_edit:
            # Aktualizacja istniejącej pozycji
            for i, item in enumerate(self.items):
                if item.get("item_id") == item_id:
                    self.items[i] = item_data
                    break
        else:
            # Dodanie nowej pozycji
            self.items.append(item_data)

        # Odświeżenie widoku
        self.refresh_items()

        # Aktualizacja kwoty faktury
        self.update_invoice_amount()

        # Zamknięcie okna dialogowego
        dialog.destroy()

    def update_invoice_amount(self):
        """Aktualizacja kwoty faktury na podstawie pozycji."""
        total = sum(item.get("quantity", 0) * item.get("unit_price", 0) for item in self.items)
        self.amount.set(f"{total:.2f}")

    def save_invoice(self, dialog):
        """Zapisanie danych faktury."""
        # Walidacja danych
        if not self.customer_combobox.get():
            messagebox.showerror("Błąd", "Wybierz klienta.")
            return

        try:
            if self.date.get():
                datetime.strptime(self.date.get(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Błąd", "Nieprawidłowy format daty wystawienia (RRRR-MM-DD).")
            return

        try:
            if self.due_date.get():
                datetime.strptime(self.due_date.get(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Błąd", "Nieprawidłowy format terminu płatności (RRRR-MM-DD).")
            return

        try:
            float(self.amount.get())
        except ValueError:
            messagebox.showerror("Błąd", "Nieprawidłowa wartość kwoty faktury.")
            return

        # Pobranie ID klienta z comboboxa
        customer_id = self.customer_combobox.get().split(" - ")[0] if self.customer_combobox.get() else ""

        # Przygotowanie danych faktury
        self.result = {
            "invoice_id": self.invoice_id.get(),
            "customer_id": customer_id,
            "date": self.date.get(),
            "due_date": self.due_date.get(),
            "amount": float(self.amount.get()),
            "currency": self.currency.get(),
            "status": self.status.get(),
            "items": self.items,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        dialog.destroy()
