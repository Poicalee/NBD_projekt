import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import uuid
from datetime import datetime
import re


class UserInterface():
    def __init__(self, root, db):
        """Inicjalizacja interfejsu użytkownika systemu księgowego."""
        self.root = root
        self.db = db
        self.root.title("System Zarządzania Księgowością")
        self.root.geometry("1000x600")

        # Zakładki dla różnych typów dokumentów
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tworzenie zakładek dla każdego typu dokumentu
        self.invoices_tab = ttk.Frame(self.notebook)
        self.transactions_tab = ttk.Frame(self.notebook)
        self.customers_tab = ttk.Frame(self.notebook)
        self.users_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.invoices_tab, text="Faktury")
        self.notebook.add(self.transactions_tab, text="Transakcje")
        self.notebook.add(self.customers_tab, text="Klienci")
        self.notebook.add(self.users_tab, text="Użytkownicy")

        # Inicjalizacja interfejsów dla każdego typu dokumentu
        self.init_invoices_ui()
        self.init_transactions_ui()
        self.init_customers_ui()
        self.init_users_ui()

    def init_invoices_ui(self):
        """Inicjalizacja interfejsu dla zakładki faktury."""
        # Główna ramka
        frame = ttk.Frame(self.invoices_tab, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # Górna ramka dla operacji
        operations_frame = ttk.Frame(frame)
        operations_frame.pack(fill=tk.X, pady=10)

        # Przyciski operacji CRUD
        ttk.Button(operations_frame, text="Dodaj fakturę", command=self.create_invoice).pack(side=tk.LEFT, padx=5)
        ttk.Button(operations_frame, text="Szczegóły faktury", command=self.view_invoice).pack(side=tk.LEFT, padx=5)
        ttk.Button(operations_frame, text="Edytuj fakturę", command=self.edit_invoice).pack(side=tk.LEFT, padx=5)
        ttk.Button(operations_frame, text="Usuń fakturę", command=self.delete_invoice).pack(side=tk.LEFT, padx=5)
        ttk.Button(operations_frame, text="Odśwież", command=self.refresh_invoices).pack(side=tk.LEFT, padx=5)

        # Lista faktur
        list_frame = ttk.LabelFrame(frame, text="Lista faktur")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Treeview dla listy faktur
        columns = ("ID", "Klient", "Data wystawienia", "Termin płatności", "Kwota", "Waluta", "Status")
        self.invoices_tree = ttk.Treeview(list_frame, columns=columns)

        self.invoices_tree.heading("#0", text="")
        self.invoices_tree.column("#0", width=0, stretch=tk.NO)

        for col in columns:
            self.invoices_tree.heading(col, text=col)
            width = 100 if col != "Klient" else 150
            self.invoices_tree.column(col, width=width)

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.invoices_tree.yview)
        self.invoices_tree.configure(yscroll=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.invoices_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Załadowanie początkowych danych
        self.refresh_invoices()

    def init_transactions_ui(self):
        """Inicjalizacja interfejsu dla zakładki transakcje."""
        # Główna ramka
        frame = ttk.Frame(self.transactions_tab, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # Górna ramka dla operacji
        operations_frame = ttk.Frame(frame)
        operations_frame.pack(fill=tk.X, pady=10)

        # Przyciski operacji CRUD
        ttk.Button(operations_frame, text="Dodaj transakcję", command=self.create_transaction).pack(side=tk.LEFT,
                                                                                                    padx=5)
        ttk.Button(operations_frame, text="Szczegóły transakcji", command=self.view_transaction).pack(side=tk.LEFT,
                                                                                                      padx=5)
        ttk.Button(operations_frame, text="Edytuj transakcję", command=self.edit_transaction).pack(side=tk.LEFT, padx=5)
        ttk.Button(operations_frame, text="Usuń transakcję", command=self.delete_transaction).pack(side=tk.LEFT, padx=5)
        ttk.Button(operations_frame, text="Odśwież", command=self.refresh_transactions).pack(side=tk.LEFT, padx=5)

        # Lista transakcji
        list_frame = ttk.LabelFrame(frame, text="Lista transakcji")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Treeview dla listy transakcji
        columns = ("ID", "ID Faktury", "Data transakcji", "Kwota", "Metoda płatności", "Status")
        self.transactions_tree = ttk.Treeview(list_frame, columns=columns)

        self.transactions_tree.heading("#0", text="")
        self.transactions_tree.column("#0", width=0, stretch=tk.NO)

        for col in columns:
            self.transactions_tree.heading(col, text=col)
            self.transactions_tree.column(col, width=120)

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.transactions_tree.yview)
        self.transactions_tree.configure(yscroll=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.transactions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Załadowanie początkowych danych
        self.refresh_transactions()

    def init_customers_ui(self):
        """Inicjalizacja interfejsu dla zakładki klienci."""
        # Główna ramka
        frame = ttk.Frame(self.customers_tab, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # Górna ramka dla operacji
        operations_frame = ttk.Frame(frame)
        operations_frame.pack(fill=tk.X, pady=10)

        # Przyciski operacji CRUD
        ttk.Button(operations_frame, text="Dodaj klienta", command=self.create_customer).pack(side=tk.LEFT, padx=5)
        ttk.Button(operations_frame, text="Szczegóły klienta", command=self.view_customer).pack(side=tk.LEFT, padx=5)
        ttk.Button(operations_frame, text="Edytuj klienta", command=self.edit_customer).pack(side=tk.LEFT, padx=5)
        ttk.Button(operations_frame, text="Usuń klienta", command=self.delete_customer).pack(side=tk.LEFT, padx=5)
        ttk.Button(operations_frame, text="Odśwież", command=self.refresh_customers).pack(side=tk.LEFT, padx=5)

        # Lista klientów
        list_frame = ttk.LabelFrame(frame, text="Lista klientów")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Treeview dla listy klientów
        columns = ("ID", "Nazwa", "Email", "Telefon", "Miasto")
        self.customers_tree = ttk.Treeview(list_frame, columns=columns)

        self.customers_tree.heading("#0", text="")
        self.customers_tree.column("#0", width=0, stretch=tk.NO)

        for col in columns:
            self.customers_tree.heading(col, text=col)
            width = 100 if col != "Nazwa" else 200
            self.customers_tree.column(col, width=width)

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.customers_tree.yview)
        self.customers_tree.configure(yscroll=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.customers_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Załadowanie początkowych danych
        self.refresh_customers()

    def init_users_ui(self):
        """Inicjalizacja interfejsu dla zakładki użytkownicy."""
        # Główna ramka
        frame = ttk.Frame(self.users_tab, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # Górna ramka dla operacji
        operations_frame = ttk.Frame(frame)
        operations_frame.pack(fill=tk.X, pady=10)

        # Przyciski operacji CRUD
        ttk.Button(operations_frame, text="Dodaj użytkownika", command=self.create_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(operations_frame, text="Szczegóły użytkownika", command=self.view_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(operations_frame, text="Edytuj użytkownika", command=self.edit_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(operations_frame, text="Usuń użytkownika", command=self.delete_user).pack(side=tk.LEFT, padx=5)
        ttk.Button(operations_frame, text="Odśwież", command=self.refresh_users).pack(side=tk.LEFT, padx=5)

        # Lista użytkowników
        list_frame = ttk.LabelFrame(frame, text="Lista użytkowników")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Treeview dla listy użytkowników
        columns = ("ID", "Nazwa użytkownika", "Rola", "Email", "Data utworzenia")
        self.users_tree = ttk.Treeview(list_frame, columns=columns)

        self.users_tree.heading("#0", text="")
        self.users_tree.column("#0", width=0, stretch=tk.NO)

        for col in columns:
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=150)

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.users_tree.yview)
        self.users_tree.configure(yscroll=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.users_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Załadowanie początkowych danych
        self.refresh_users()

    # ==================== Metody dla faktur ====================

    def refresh_invoices(self):
        """Odświeżenie listy faktur."""
        # Wyczyszczenie listy
        for item in self.invoices_tree.get_children():
            self.invoices_tree.delete(item)

        # Pobranie kluczy faktur
        keys = self.db.list_keys("invoices")

        for key in keys:
            invoice = self.db.read("invoices", key)
            if invoice:
                # Pobranie nazwy klienta
                customer_name = "Nieznany"
                if "customer_id" in invoice:
                    customer = self.db.read("customers", "customer:" + invoice["customer_id"])
                    if customer:
                        customer_name = customer.get("name", "Nieznany")

                self.invoices_tree.insert("", tk.END, values=(
                    key.replace("invoice:", ""),
                    customer_name,
                    invoice.get("date", ""),
                    invoice.get("due_date", ""),
                    invoice.get("amount", 0),
                    invoice.get("currency", "PLN"),
                    invoice.get("status", "")
                ))

    def create_invoice(self):
        """Utworzenie nowej faktury."""
        dialog = InvoiceDialog(self.root, "Dodaj nową fakturę", self.db)
        if dialog.result:
            invoice_id = dialog.result.get("invoice_id")
            key = f"invoice:{invoice_id}"
            if self.db.create("invoices", key, dialog.result):
                messagebox.showinfo("Sukces", "Faktura została dodana pomyślnie")
                self.refresh_invoices()
            else:
                messagebox.showerror("Błąd", "Nie udało się dodać faktury")

    def view_invoice(self):
        """Wyświetlenie szczegółów faktury."""
        selected = self.invoices_tree.selection()
        if not selected:
            messagebox.showwarning("Ostrzeżenie", "Wybierz fakturę do wyświetlenia")
            return

        invoice_id = self.invoices_tree.item(selected[0])["values"][0]
        key = f"invoice:{invoice_id}"
        invoice = self.db.read("invoices", key)

        if invoice:
            # Utworzenie okna dialogowego ze szczegółami
            details_window = tk.Toplevel(self.root)
            details_window.title(f"Szczegóły faktury {invoice_id}")
            details_window.geometry("600x500")

            frame = ttk.Frame(details_window, padding="20")
            frame.pack(fill=tk.BOTH, expand=True)

            # Podstawowe informacje
            ttk.Label(frame, text="Szczegóły faktury", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2,
                                                                                    sticky="w", pady=(0, 20))

            basic_info = ttk.LabelFrame(frame, text="Podstawowe informacje")
            basic_info.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)

            # Wyświetlenie podstawowych informacji o fakturze
            ttk.Label(basic_info, text="ID faktury:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
            ttk.Label(basic_info, text=invoice_id).grid(row=0, column=1, sticky="w", padx=5, pady=2)

            ttk.Label(basic_info, text="ID klienta:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
            ttk.Label(basic_info, text=invoice.get("customer_id", "")).grid(row=1, column=1, sticky="w", padx=5, pady=2)

            ttk.Label(basic_info, text="Data wystawienia:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
            ttk.Label(basic_info, text=invoice.get("date", "")).grid(row=2, column=1, sticky="w", padx=5, pady=2)

            ttk.Label(basic_info, text="Termin płatności:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
            ttk.Label(basic_info, text=invoice.get("due_date", "")).grid(row=3, column=1, sticky="w", padx=5, pady=2)

            ttk.Label(basic_info, text="Kwota:").grid(row=4, column=0, sticky="w", padx=5, pady=2)
            ttk.Label(basic_info, text=f"{invoice.get('amount', 0)} {invoice.get('currency', 'PLN')}").grid(row=4,
                                                                                                            column=1,
                                                                                                            sticky="w",
                                                                                                            padx=5,
                                                                                                            pady=2)

            ttk.Label(basic_info, text="Status:").grid(row=5, column=0, sticky="w", padx=5, pady=2)
            ttk.Label(basic_info, text=invoice.get("status", "")).grid(row=5, column=1, sticky="w", padx=5, pady=2)

            # Pozycje faktury
            items_frame = ttk.LabelFrame(frame, text="Pozycje faktury")
            items_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)

            # Treeview dla pozycji faktury
            columns = ("ID", "Opis", "Ilość", "Cena jedn.", "Wartość")
            items_tree = ttk.Treeview(items_frame, columns=columns)

            items_tree.heading("#0", text="")
            items_tree.column("#0", width=0, stretch=tk.NO)

            for col in columns:
                items_tree.heading(col, text=col)
                items_tree.column(col, width=100)

            # Wypełnienie danych pozycji
            for item in invoice.get("items", []):
                value = item.get("quantity", 0) * item.get("unit_price", 0)
                items_tree.insert("", tk.END, values=(
                    item.get("item_id", ""),
                    item.get("description", ""),
                    item.get("quantity", 0),
                    item.get("unit_price", 0),
                    value
                ))

            # Scrollbar dla pozycji
            scrollbar = ttk.Scrollbar(items_frame, orient="vertical", command=items_tree.yview)
            items_tree.configure(yscroll=scrollbar.set)

            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            items_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Przyciski
            button_frame = ttk.Frame(frame)
            button_frame.grid(row=3, column=0, columnspan=2, sticky="e", pady=20)

            ttk.Button(button_frame, text="Zamknij", command=details_window.destroy).pack(side=tk.RIGHT)

            # Konfiguracja wagi wierszy i kolumn
            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(2, weight=1)
        else:
            messagebox.showerror("Błąd", "Nie znaleziono faktury")

    def edit_invoice(self):
        """Edycja istniejącej faktury."""
        selected = self.invoices_tree.selection()
        if not selected:
            messagebox.showwarning("Ostrzeżenie", "Wybierz fakturę do edycji")
            return

        invoice_id = self.invoices_tree.item(selected[0])["values"][0]
        key = f"invoice:{invoice_id}"
        invoice = self.db.read("invoices", key)

        if invoice:
            dialog = InvoiceDialog(self.root, "Edytuj fakturę", self.db, invoice)
            if dialog.result:
                if self.db.update("invoices", key, dialog.result):
                    messagebox.showinfo("Sukces", "Faktura została zaktualizowana pomyślnie")
                    self.refresh_invoices()
                else:
                    messagebox.showerror("Błąd", "Nie udało się zaktualizować faktury")
        else:
            messagebox.showerror("Błąd", "Nie znaleziono faktury")

    def delete_invoice(self):
        """Usunięcie faktury."""
        selected = self.invoices_tree.selection()
        if not selected:
            messagebox.showwarning("Ostrzeżenie", "Wybierz fakturę do usunięcia")
            return

        invoice_id = self.invoices_tree.item(selected[0])["values"][0]
        key = f"invoice:{invoice_id}"

        if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć tę fakturę?"):
            if self.db.delete("invoices", key):
                messagebox.showinfo("Sukces", "Faktura została usunięta pomyślnie")
                self.refresh_invoices()
            else:
                messagebox.showerror("Błąd", "Nie udało się usunąć faktury")

    # ==================== Metody dla transakcji ====================

    def refresh_transactions(self):
        """Odświeżenie listy transakcji."""
        # Wyczyszczenie listy
        for item in self.transactions_tree.get_children():
            self.transactions_tree.delete(item)

        # Pobranie kluczy transakcji
        keys = self.db.list_keys("transactions")

        for key in keys:
            transaction = self.db.read("transactions", key)
            if transaction:
                self.transactions_tree.insert("", tk.END, values=(
                    key.replace("transaction:", ""),
                    transaction.get("invoice_id", ""),
                    transaction.get("transaction_date", ""),
                    transaction.get("amount", 0),
                    transaction.get("payment_method", ""),
                    transaction.get("status", "")
                ))

    def create_transaction(self):
        """Utworzenie nowej transakcji."""
        dialog = TransactionDialog(self.root, "Dodaj nową transakcję", self.db)
        if dialog.result:
            transaction_id = dialog.result.get("transaction_id")
            key = f"transaction:{transaction_id}"
            if self.db.create("transactions", key, dialog.result):
                messagebox.showinfo("Sukces", "Transakcja została dodana pomyślnie")
                self.refresh_transactions()
            else:
                messagebox.showerror("Błąd", "Nie udało się dodać transakcji")

    def view_transaction(self):
        """Wyświetlenie szczegółów transakcji."""
        selected = self.transactions_tree.selection()
        if not selected:
            messagebox.showwarning("Ostrzeżenie", "Wybierz transakcję do wyświetlenia")
            return

        transaction_id = self.transactions_tree.item(selected[0])["values"][0]
        key = f"transaction:{transaction_id}"
        transaction = self.db.read("transactions", key)

        if transaction:
            # Tworzenie listy szczegółów
            details = []
            details.append(f"ID transakcji: {transaction_id}")
            details.append(f"ID faktury: {transaction.get('invoice_id', '')}")
            details.append(f"Data transakcji: {transaction.get('transaction_date', '')}")
            details.append(f"Kwota: {transaction.get('amount', 0)}")
            details.append(f"Metoda płatności: {transaction.get('payment_method', '')}")
            details.append(f"Status: {transaction.get('status', '')}")
            details.append(f"Numer referencyjny: {transaction.get('reference_number', '')}")
            details.append(f"Data utworzenia: {transaction.get('created_at', '')}")

            messagebox.showinfo("Szczegóły transakcji", "\n".join(details))
        else:
            messagebox.showerror("Błąd", "Nie znaleziono transakcji")

    def edit_transaction(self):
        """Edycja istniejącej transakcji."""
        selected = self.transactions_tree.selection()
        if not selected:
            messagebox.showwarning("Ostrzeżenie", "Wybierz transakcję do edycji")
            return

        transaction_id = self.transactions_tree.item(selected[0])["values"][0]
        key = f"transaction:{transaction_id}"
        transaction = self.db.read("transactions", key)

        if transaction:
            dialog = TransactionDialog(self.root, "Edytuj transakcję", self.db, transaction)
            if dialog.result:
                if self.db.update("transactions", key, dialog.result):
                    messagebox.showinfo("Sukces", "Transakcja została zaktualizowana pomyślnie")
                    self.refresh_transactions()
                else:
                    messagebox.showerror("Błąd", "Nie udało się zaktualizować transakcji")
        else:
            messagebox.showerror("Błąd", "Nie znaleziono transakcji")

    def delete_transaction(self):
        """Usunięcie transakcji."""
        selected = self.transactions_tree.selection()
        if not selected:
            messagebox.showwarning("Ostrzeżenie", "Wybierz transakcję do usunięcia")
            return

        transaction_id = self.transactions_tree.item(selected[0])["values"][0]
        key = f"transaction:{transaction_id}"

        if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć tę transakcję?"):
            if self.db.delete("transactions", key):
                messagebox.showinfo("Sukces", "Transakcja została usunięta pomyślnie")
                self.refresh_transactions()
            else:
                messagebox.showerror("Błąd", "Nie udało się usunąć transakcji")

    # ==================== Metody dla klientów ====================

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

    class UserDialog:
        """Dialog dodawania/edycji użytkownika."""

        def __init__(self, parent, title, user=None):
            self.result = None

            # Tworzenie okna dialogowego
            dialog = tk.Toplevel(parent)
            dialog.title(title)
            dialog.geometry("500x400")
            dialog.transient(parent)
            dialog.resizable(False, False)

            frame = ttk.Frame(dialog, padding="20")
            frame.pack(fill=tk.BOTH, expand=True)

            # Pola formularza
            ttk.Label(frame, text="Dane użytkownika", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2,
                                                                                   sticky="w", pady=(0, 15))

            # ID użytkownika
            self.user_id = tk.StringVar(value=user.get("user_id", str(uuid.uuid4())) if user else str(uuid.uuid4()))

            # Nazwa użytkownika
            ttk.Label(frame, text="Nazwa użytkownika:").grid(row=1, column=0, sticky="w", pady=5)
            self.username = tk.StringVar(value=user.get("username", "") if user else "")
            ttk.Entry(frame, textvariable=self.username, width=40).grid(row=1, column=1, sticky="ew", pady=5)

            # Email
            ttk.Label(frame, text="Email:").grid(row=2, column=0, sticky="w", pady=5)
            self.email = tk.StringVar(value=user.get("email", "") if user else "")
            ttk.Entry(frame, textvariable=self.email, width=40).grid(row=2, column=1, sticky="ew", pady=5)

            # Hasło (jeśli nowy użytkownik)
            if not user:
                ttk.Label(frame, text="Hasło:").grid(row=3, column=0, sticky="w", pady=5)
                self.password = tk.StringVar()
                ttk.Entry(frame, textvariable=self.password, show="*", width=40).grid(row=3, column=1, sticky="ew",
                                                                                      pady=5)
            else:
                self.password = None

            # Rola
            ttk.Label(frame, text="Rola:").grid(row=4, column=0, sticky="w", pady=5)
            self.role = tk.StringVar(value=user.get("role", "użytkownik") if user else "użytkownik")
            roles = ["administrator", "księgowy", "użytkownik"]
            ttk.Combobox(frame, textvariable=self.role, values=roles, state="readonly").grid(row=4, column=1,
                                                                                             sticky="ew", pady=5)

            # Aktywność
            ttk.Label(frame, text="Aktywny:").grid(row=5, column=0, sticky="w", pady=5)
            self.is_active = tk.BooleanVar(value=user.get("is_active", True) if user else True)
            ttk.Checkbutton(frame, variable=self.is_active).grid(row=5, column=1, sticky="w", pady=5)

            # Przyciski
            button_frame = ttk.Frame(frame)
            button_frame.grid(row=6, column=0, columnspan=2, sticky="e", pady=(20, 0))

            ttk.Button(button_frame, text="Anuluj", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
            ttk.Button(button_frame, text="Zapisz", command=lambda: self.save_user(dialog)).pack(side=tk.RIGHT)

            # Konfiguracja wagi kolumn
            frame.columnconfigure(1, weight=1)

            # Ustawienie modalności
            dialog.grab_set()
            parent.wait_window(dialog)

        def save_user(self, dialog):
            """Zapisanie danych użytkownika."""
            # Walidacja danych
            if not self.username.get().strip():
                messagebox.showerror("Błąd", "Nazwa użytkownika jest wymagana.")
                return

            # Walidacja emaila
            email = self.email.get().strip()
            if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                messagebox.showerror("Błąd", "Nieprawidłowy format adresu email.")
                return

            # Walidacja hasła
            if self.password is not None and not self.password.get():
                messagebox.showerror("Błąd", "Hasło jest wymagane.")
                return

            # Przygotowanie danych użytkownika
            self.result = {
                "user_id": self.user_id.get(),
                "username": self.username.get().strip(),
                "email": self.email.get().strip(),
                "role": self.role.get(),
                "is_active": self.is_active.get()
            }

            # Dodanie hasła dla nowego użytkownika
            if self.password is not None:
                # W rzeczywistej aplikacji należałoby zahashować hasło
                self.result["password"] = self.password.get()

            dialog.destroy()


class InvoiceDialog:
    """Dialog dodawania/edycji faktury."""

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

        # Data wystawienia
        ttk.Label(frame, text="Data wystawienia:").grid(row=2, column=0, sticky="w", pady=5)
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
            amount = float(self.amount.get())
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


class TransactionDialog:
    """Dialog dodawania/edycji transakcji."""

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

        # Data transakcji
        ttk.Label(frame, text="Data transakcji:").grid(row=2, column=0, sticky="w", pady=5)
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