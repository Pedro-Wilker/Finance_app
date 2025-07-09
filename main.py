import customtkinter as ctk
from gui.app import FinanceApp

if __name__ == "__main__":
    root = ctk.CTk()
    app = FinanceApp(root)
    root.mainloop()