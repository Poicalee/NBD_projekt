import tkinter as tk
from tkinter import ttk, messagebox
import uuid
from datetime import datetime
import re
from app.methods.customers_operations import CustomerOperations
from app.methods.invoices_operations import InvoiceOperations
from app.methods.transactions_operations import TransactionsOperations
from app.methods.users_operations import UsersOperations
from app.Dialog.transaction_dialog import TransactionDialog
from app.Dialog.invoice_dialog import InvoiceDialog

# noinspection PyArgumentList
class UserInterface:
    def __init__(self, root, db):
        """Inicjalizacja interfejsu użytkownika systemu księgowego."""
        self.users_tree = None
        self.customers_tree = None
        self.customers_tree = None
        self.transactions_tree = None
        self.invoices_tree = None
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
        self.operations = InvoiceOperations(self)
        self.init_invoices_ui()
        self.operations = TransactionsOperations(self)
        self.init_transactions_ui()
        self.operations = CustomerOperations(self)
        self.init_customers_ui()
        self.operations = UsersOperations(self)
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
        ttk.Button(operations_frame, text="Dodaj fakturę", command=self.operations.create_invoice).pack(side=tk.LEFT,
                                                                                                        padx=5)
        ttk.Button(operations_frame, text="Szczegóły faktury", command=self.operations.view_invoice).pack(side=tk.LEFT,
                                                                                                          padx=5)
        ttk.Button(operations_frame, text="Edytuj fakturę", command=self.operations.edit_invoice).pack(side=tk.LEFT,
                                                                                                       padx=5)
        ttk.Button(operations_frame, text="Usuń fakturę", command=self.operations.delete_invoice).pack(side=tk.LEFT,
                                                                                                       padx=5)
        ttk.Button(operations_frame, text="Odśwież", command=self.operations.refresh_invoices).pack(side=tk.LEFT,
                                                                                                    padx=5)

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
        self.operations.refresh_invoices()

    def init_transactions_ui(self):
        """Inicjalizacja interfejsu dla zakładki transakcje."""
        # Główna ramka
        frame = ttk.Frame(self.transactions_tab, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # Górna ramka dla operacji
        operations_frame = ttk.Frame(frame)
        operations_frame.pack(fill=tk.X, pady=10)

        # Przyciski operacji CRUD
        ttk.Button(operations_frame, text="Dodaj transakcję", command=self.operations.create_transaction).pack(
            side=tk.LEFT,
            padx=5)
        ttk.Button(operations_frame, text="Szczegóły transakcji", command=self.operations.view_transaction).pack(
            side=tk.LEFT,
            padx=5)
        ttk.Button(operations_frame, text="Edytuj transakcję", command=self.operations.edit_transaction).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(operations_frame, text="Usuń transakcję", command=self.operations.delete_transaction).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(operations_frame, text="Odśwież", command=self.operations.refresh_transactions).pack(side=tk.LEFT,
                                                                                                        padx=5)

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
        self.operations.refresh_transactions()

    def init_customers_ui(self):
        """Inicjalizacja interfejsu dla zakładki klienci."""
        # Główna ramka
        frame = ttk.Frame(self.customers_tab, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # Górna ramka dla operacji
        operations_frame = ttk.Frame(frame)
        operations_frame.pack(fill=tk.X, pady=10)

        # Przyciski operacji CRUD
        ttk.Button(operations_frame, text="Dodaj klienta", command=self.operations.create_customer).pack(side=tk.LEFT,
                                                                                                         padx=5)
        ttk.Button(operations_frame, text="Szczegóły klienta", command=self.operations.view_customers).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(operations_frame, text="Edytuj klienta", command=self.operations.edit_customer).pack(side=tk.LEFT,
                                                                                                        padx=5)
        ttk.Button(operations_frame, text="Usuń klienta", command=self.operations.delete_customer).pack(side=tk.LEFT,
                                                                                                        padx=5)
        ttk.Button(operations_frame, text="Odśwież", command=self.operations.refresh_customers).pack(side=tk.LEFT,
                                                                                                     padx=5)

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
        self.operations.refresh_customers()

    def init_users_ui(self):
        """Inicjalizacja interfejsu dla zakładki użytkownicy."""
        # Główna ramka
        frame = ttk.Frame(self.users_tab, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # Górna ramka dla operacji
        operations_frame = ttk.Frame(frame)
        operations_frame.pack(fill=tk.X, pady=10)

        # Przyciski operacji CRUD
        ttk.Button(operations_frame, text="Dodaj użytkownika", command=self.operations.create_user).pack(side=tk.LEFT,
                                                                                                         padx=5)
        ttk.Button(operations_frame, text="Szczegóły użytkownika", command=self.operations.view_user).pack(side=tk.LEFT,
                                                                                                           padx=5)
        ttk.Button(operations_frame, text="Edytuj użytkownika", command=self.operations.edit_user).pack(side=tk.LEFT,
                                                                                                        padx=5)
        ttk.Button(operations_frame, text="Usuń użytkownika", command=self.operations.delete_user).pack(side=tk.LEFT,
                                                                                                        padx=5)
        ttk.Button(operations_frame, text="Odśwież", command=self.operations.refresh_users).pack(side=tk.LEFT, padx=5)

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
        self.operations.refresh_users()
