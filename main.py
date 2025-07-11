import customtkinter as ctk
from gui.app import FinanceApp
import uvicorn
from threading import Thread

def start_api():
    uvicorn.run("backend.api:app", host="localhost", port=8000, reload=False)

if __name__ == "__main__":
    Thread(target=start_api).start()
    root = ctk.CTk()
    app = FinanceApp(root)
    root.mainloop()