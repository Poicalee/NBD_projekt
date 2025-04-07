from tkinter import messagebox, ttk
import tkinter as tk


class InvoiceOperations:
    def __init__(self, ui):
        self.ui = ui
        self.root = ui.root
        self.db = ui.db

    def refresh_invoices(self):
        """Odświeżenie listy faktur."""
        # Wyczyszczenie listy
        for item in self.ui.invoices_tree.get_children():
            self.ui.invoices_tree.delete(item)

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

                self.ui.invoices_tree.insert("", tk.END, values=(
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
        from app.UI.ui import InvoiceDialog
        dialog = InvoiceDialog(self.root, "Dodaj nową fakturę", self.db)
        if dialog.result:
            invoice_id = dialog.result.get("invoice_id")
            key = f"invoice:{invoice_id}"
            if self.db.create("invoices", key, dialog.result):
                messagebox.showinfo("Sukces", "Faktura została dodana pomyślnie")
                self.refresh_invoices()
            else:
                messagebox.showerror("Błąd", "Nie udało się dodać faktury")

    # noinspection PyArgumentList
    def view_invoice(self):
        """Wyświetlenie szczegółów faktury."""
        selected = self.ui.invoices_tree.selection()
        if not selected:
            messagebox.showwarning("Ostrzeżenie", "Wybierz fakturę do wyświetlenia")
            return

        invoice_id = self.ui.invoices_tree.item(selected[0])["values"][0]
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
        selected = self.ui.invoices_tree.selection()
        if not selected:
            messagebox.showwarning("Ostrzeżenie", "Wybierz fakturę do edycji")
            return

        invoice_id = self.ui.invoices_tree.item(selected[0])["values"][0]
        key = f"invoice:{invoice_id}"
        invoice = self.db.read("invoices", key)

        if invoice:
            from app.UI.ui import InvoiceDialog
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
        selected = self.ui.invoices_tree.selection()
        if not selected:
            messagebox.showwarning("Ostrzeżenie", "Wybierz fakturę do usunięcia")
            return

        invoice_id = self.ui.invoices_tree.item(selected[0])["values"][0]
        key = f"invoice:{invoice_id}"

        if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć tę fakturę?"):
            if self.db.delete("invoices", key):
                messagebox.showinfo("Sukces", "Faktura została usunięta pomyślnie")
                self.refresh_invoices()
            else:
                messagebox.showerror("Błąd", "Nie udało się usunąć faktury")
