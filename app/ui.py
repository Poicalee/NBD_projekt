import tkinter as tk
from tkinter import messagebox


def start_gui(client):
    def test_connection():
        if client.ping():
            messagebox.showinfo("Połączenie", "Połączono z Riak!")
        else:
            messagebox.showerror("Błąd", "Nie udało się połączyć z Riak")

    root = tk.Tk()
    root.title("System Zarządzania Księgowością")
    root.geometry("400x300")

    label = tk.Label(root, text="System Zarządzania Księgowością", font=("Arial", 14))
    label.pack(pady=20)

    btn_test = tk.Button(root, text="Testuj połączenie", command=test_connection)
    btn_test.pack(pady=10)

    btn_exit = tk.Button(root, text="Zamknij", command=root.quit)
    btn_exit.pack(pady=10)

    root.mainloop()