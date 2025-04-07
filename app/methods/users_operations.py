from tkinter import messagebox
import tkinter as tk


class UsersOperations:
    def __init__(self, ui):
        self.ui = ui
        self.root = ui.root
        self.db = ui.db

    def refresh_users(self):
        """Odświeżenie listy użytkowników."""
        # Wyczyszczenie listy
        for item in self.ui.users_tree.get_children():
            self.ui.users_tree.delete(item)

        keys = self.db.list_keys("users")

        for key in keys:
            user = self.db.read("users", key)
            if user:
                status = "Aktywny" if user.get("is_acitve", False) else "Niekontywny"
                self.ui.users_tree.insert("", tk.END, values=(
                    key.replace("user:", ""),
                    user.get("username", ""),
                    user.get("email", ""),
                    user.get("role", ""),
                    status
                ))

    def create_user(self):
        """Utworzenie nowego użytkownika"""
        dialog = self.ui.UserDialog(self.root, "Dodaj nowego użytkownika")
        if dialog.result:
            user_id = dialog.result.get("user_id")
            key = f"user/{user_id}"
            if self.db.create("users", key, dialog.result):
                messagebox.showinfo("Sukces", "Użytkownik został dodany pomyślnie")
                self.refresh_users()
            else:
                messagebox.showerror("Błąd", "Nie udało się dodać użytkownika")

    def view_user(self):
        """Wyświetlenie szczegółów użytkownika."""
        selected = self.ui.users_tree.selection()
        if not selected:
            messagebox.showwarning("Ostrzeżenie", "Wybierz użytkownika do wyświetlenia")
            return

        user_id = self.ui.users_tree.item(selected[0])["values"][0]
        key = f"user:{user_id}"
        user = self.db.read("users", key)

        if user:
            # Tworzenie listy szczegółów
            details = [f"ID użytkownika: {user_id}", f"Nazwa użytkownika: {user.get('username', '')}",
                       f"Email: {user.get('email', '')}", f"Rola: {user.get('role', '')}",
                       f"Status: {'Aktywny' if user.get('is_active', False) else 'Nieaktywny'}"]

            messagebox.showinfo("Szczegóły użytkownika", "\n".join(details))
        else:
            messagebox.showerror("Błąd", "Nie znaleziono użytkownika")

    def edit_user(self):
        """Edycja istniejącego użytkownika."""
        selected = self.ui.users_tree.selection()
        if not selected:
            messagebox.showwarning("Ostrzeżenie", "Wybierz użytkownika do edycji")
            return

        user_id = self.ui.users_tree.item(selected[0])["values"][0]
        key = f"user:{user_id}"
        user = self.db.read("users", key)

        if user:
            dialog = self.ui.UserDialog(self.root, "Edytuj użytkownika", user)
            if dialog.result:
                if self.db.update("users", key, dialog.result):
                    messagebox.showinfo("Sukces", "Użytkownik został zaktualizowany pomyślnie")
                    self.refresh_users()
                else:
                    messagebox.showerror("Błąd", "Nie udało się zaktualizować użytkownika")
        else:
            messagebox.showerror("Błąd", "Nie znaleziono użytkownika")

    def delete_user(self):
        """Usunięcie użytkownika."""
        selected = self.ui.users_tree.selection()
        if not selected:
            messagebox.showwarning("Ostrzeżenie", "Wybierz użytkownika do usunięcia")
            return

        user_id = self.ui.users_tree.item(selected[0])["values"][0]
        key = f"user:{user_id}"

        if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć tego użytkownika?"):
            if self.db.delete("users", key):
                messagebox.showinfo("Sukces", "Użytkownik został usunięty pomyślnie")
                self.refresh_users()
            else:
                messagebox.showerror("Błąd", "Nie udało się usunąć użytkownika")
