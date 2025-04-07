from tkinter import messagebox
import tkinter as tk


class TransactionsOperations:
    def __init__(self, ui):
        self.ui = ui
        self.root = ui.root
        self.db = ui.db

    def refresh_transactions(self):
        """Odświeżenie listy transakcji."""
        # Wyczyszczenie listy
        for item in self.ui.transactions_tree.get_children():
            self.ui.transactions_tree.delete(item)

        # Pobranie kluczy transakcji
        keys = self.db.list_keys("transactions")

        for key in keys:
            transaction = self.db.read("transactions", key)
            if transaction:
                self.ui.transactions_tree.insert("", tk.END, values=(
                    key.replace("transaction:", ""),
                    transaction.get("invoice_id", ""),
                    transaction.get("transaction_date", ""),
                    transaction.get("amount", 0),
                    transaction.get("payment_method", ""),
                    transaction.get("status", "")
                ))

    def create_transaction(self):
        """Utworzenie nowej transakcji."""
        from app.UI.ui import TransactionDialog
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
        selected = self.ui.transactions_tree.selection()
        if not selected:
            messagebox.showwarning("Ostrzeżenie", "Wybierz transakcję do wyświetlenia")
            return

        transaction_id = self.ui.transactions_tree.item(selected[0])["values"][0]
        key = f"transaction:{transaction_id}"
        transaction = self.db.read("transactions", key)

        if transaction:
            # Tworzenie listy szczegółów
            details = [f"ID transakcji: {transaction_id}", f"ID faktury: {transaction.get('invoice_id', '')}",
                       f"Data transakcji: {transaction.get('transaction_date', '')}",
                       f"Kwota: {transaction.get('amount', 0)}",
                       f"Metoda płatności: {transaction.get('payment_method', '')}",
                       f"Status: {transaction.get('status', '')}",
                       f"Numer referencyjny: {transaction.get('reference_number', '')}",
                       f"Data utworzenia: {transaction.get('created_at', '')}"]

            messagebox.showinfo("Szczegóły transakcji", "\n".join(details))
        else:
            messagebox.showerror("Błąd", "Nie znaleziono transakcji")

    def edit_transaction(self):
        """Edycja istniejącej transakcji."""
        selected = self.ui.transactions_tree.selection()
        if not selected:
            messagebox.showwarning("Ostrzeżenie", "Wybierz transakcję do edycji")
            return

        transaction_id = self.ui.transactions_tree.item(selected[0])["values"][0]
        key = f"transaction:{transaction_id}"
        transaction = self.db.read("transactions", key)

        if transaction:
            from app.UI.ui import TransactionDialog
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
        selected = self.ui.transactions_tree.selection()
        if not selected:
            messagebox.showwarning("Ostrzeżenie", "Wybierz transakcję do usunięcia")
            return

        transaction_id = self.ui.transactions_tree.item(selected[0])["values"][0]
        key = f"transaction:{transaction_id}"

        if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć tę transakcję?"):
            if self.db.delete("transactions", key):
                messagebox.showinfo("Sukces", "Transakcja została usunięta pomyślnie")
                self.refresh_transactions()
            else:
                messagebox.showerror("Błąd", "Nie udało się usunąć transakcji")
