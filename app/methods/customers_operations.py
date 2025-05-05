# app/methods/customers_operations.py
from tkinter import messagebox
import tkinter as tk
from app.Dialog.customer_dialog import CustomerDialog

class CustomerOperations:
    def __init__(self, ui):
        self.ui = ui
        self.root = ui.root
        self.db = ui.db

    def refresh_customers(self):
        """Odświeżenie listy klientów."""
        # Wyczyszczenie listy
        for item in self.ui.customers_tree.get_children():
            self.ui.customers_tree.delete(item)

        # Pobranie kluczy klientów
        keys = self.db.list_keys("customers")

        for key in keys:
            customer = self.db.read("customers", key)
            if customer:
                self.ui.customers_tree.insert("", tk.END, values=(
                    key.replace("customer:", ""),
                    customer.get("name", ""),
                    customer.get("email", ""),
                    customer.get("phone", ""),
                    customer.get("city", "")
                ))

    def create_customer(self):
        """Utworzenie nowego klienta."""
        dialog = CustomerDialog(self.root, "Dodaj nowego klienta")
        if dialog.result:
            customer_id = dialog.result.get("customer_id")
            key = f"customer:{customer_id}"
            if self.db.create("customers", key, dialog.result):
                messagebox.showinfo("Sukces", "Klient został dodany pomyślnie")
                self.refresh_customers()
            else:
                messagebox.showerror("Błąd", "Nie udało się dodać klienta")

    def view_customers(self):
        """Wyświetlnie szczegółów klienta."""
        selected = self.ui.customers_tree.selection()
        if not selected:
            messagebox.showwarning("Ostrzeżenie", "Wybierz klienta do wyświetlenia")
            return

        customer_id = self.ui.customers_tree.item(selected[0])["values"][0]
        key = f"customer:{customer_id}"
        customer = self.db.read("customers", key)

        if customer:
            # Tworzenie listy szczegółów
            details = [f"ID klienta: {customer_id}", f"Nazwa: {customer.get('name', '')}",
                       f"Email: {customer.get('email', '')}", f"Telefon: {customer.get('phone', '')}",
                       f"Adres: {customer.get('address', '')}", f"Miasto: {customer.get('city', '')}",
                       f"Kod pocztowy: {customer.get('postal_code', '')}", f"NIP: {customer.get('tax_id', '')}",
                       f"Data utworzenia: {customer.get('created_at', '')}"]

            messagebox.showinfo("Szczegóły klienta", "\n".join(details))
        else:
            messagebox.showerror("Błąd", "Nie znaleziono klienta")

    def edit_customer(self):
        """Edycja istniejącego klienta."""
        selected = self.ui.customers_tree.selection()
        if not selected:
            messagebox.showwarning("Ostrzeżenie", "Wybierz klienta do edycji")
            return

        customer_id = self.ui.customers_tree.item(selected[0])["values"][0]
        key = f"customer:{customer_id}"
        customer = self.db.read("customers", key)

        if customer:
            dialog = CustomerDialog(self.root, "Edytuj klienta", customer)
            if dialog.result:
                if self.db.update("customers", key, dialog.result):
                    messagebox.showinfo("Sukces", "Klient został zaktualizowany pomyślnie")
                    self.refresh_customers()
                else:
                    messagebox.showerror("Błąd", "Nie udało się zaktualizować klienta")
        else:
            messagebox.showerror("Błąd", "Nie znaleziono klienta")

    def delete_customer(self):
        """Usunięcie klienta."""
        selected = self.ui.customers_tree.selection()
        if not selected:
            messagebox.showwarning("Ostrzeżenie", "Wybierz klienta do usunięcia")
            return

        customer_id = self.ui.customers_tree.item(selected[0])["values"][0]
        key = f"customer:{customer_id}"

        if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć tego klienta?"):
            if self.db.delete("customers", key):
                messagebox.showinfo("Sukces", "Klient został usunięty pomyślnie")
                self.refresh_customers()
            else:
                messagebox.showerror("Błąd", "Nie udało się usunąć klienta")