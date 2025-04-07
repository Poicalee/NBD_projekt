import re
from tkinter import messagebox

import tk


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

        from tkinter import ttk
        frame = ttk.Frame(dialog, padding="20")
        import tk
        frame.pack(fill=tk.BOTH, expand=True)

        # Pola formularza
        ttk.Label(frame, text="Dane użytkownika", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2,
                                                                               sticky="w", pady=(0, 15))

        # ID użytkownika
        import uuid
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
