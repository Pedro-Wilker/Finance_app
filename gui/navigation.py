import customtkinter as ctk
from PIL import Image
import os

class NavigationBar(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, height=50, fg_color="#333333")
        self.app = app
        self.grid(row=0, column=0, sticky="ew")
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        buttons = [
            ("Home", self.app.show_home_screen, "home.png"),
            ("Transações", self.app.show_transacao_screen, "transacao.png"),
            ("Custos Fixos", self.app.show_custos_fixos_screen, "custos.png"),
            ("Apostas", self.app.show_apostas_screen, "apostas.png"),
            ("Investimentos", self.app.show_investimentos_screen, "investimentos.png"),
            ("Relatório", self.app.show_relatorio_screen, "relatorio.png"),
            ("Resumo", self.app.show_resumo_screen, "resumo.png"),
        ]

        for i, (text, command, icon_name) in enumerate(buttons):
            icon_path = os.path.join("gui", "assets", icon_name)
            try:
                icon = ctk.CTkImage(Image.open(icon_path), size=(30, 30))
            except FileNotFoundError:
                print(f"Ícone não encontrado: {icon_path}. Usando botão sem ícone.")
                icon = None
            btn = ctk.CTkButton(
                self, text=text, image=icon, compound="left",
                command=command, width=150, height=40,
                corner_radius=10, font=("Roboto", 14)
            )
            btn.grid(row=0, column=i, padx=5, pady=5)