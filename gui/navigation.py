import customtkinter as ctk
from PIL import Image

class NavigationBar(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=10, fg_color="#2B2B2B")
        self.app = app
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

        buttons = [
            ("Home", "assets/home.png", self.app.show_main_screen),
            ("Transações", "assets/transacao.png", self.app.show_transacao_screen),
            ("Custos Fixos", "assets/custos.png", self.app.show_custos_fixos_screen),
            ("Apostas", "assets/apostas.png", self.app.show_apostas_screen),
            ("Relatório", "assets/relatorio.png", self.app.show_relatorio_screen),
            ("Resumo", "assets/resumo.png", self.app.show_resumo_screen),
            ("Investimentos", "assets/investimentos.png", self.app.show_investimentos_screen)
        ]

        for i, (text, icon_path, command) in enumerate(buttons):
            icon = ctk.CTkImage(Image.open(icon_path), size=(30, 30))
            btn = ctk.CTkButton(
                self, text="", image=icon, command=command,
                width=60, height=60, corner_radius=15, fg_color="#3B3B3B",
                hover_color="#4CAF50"
            )
            btn.grid(row=0, column=i, padx=5, pady=5)
            ctk.CTkLabel(self, text=text, font=("Roboto", 12)).grid(row=1, column=i, pady=2)