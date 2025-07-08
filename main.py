from gui.app import FinanceApp
import customtkinter as ctk

if __name__ == "__main__":
    root = ctk.CTk()
    app = FinanceApp(root)
    root.mainloop()