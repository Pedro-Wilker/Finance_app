import customtkinter as ctk
import requests
from datetime import datetime, date

class HomeScreen(ctk.CTkScrollableFrame):
    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=15)
        self.app = app
        self.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.grid_columnconfigure(0, weight=1)

        # Título
        ctk.CTkLabel(self, text=f"Bem-vindo, {app.nome_usuario}!", font=("Roboto", 24, "bold")).pack(pady=20)

        # Abas
        self.tabview = ctk.CTkTabview(self, corner_radius=10)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Aba Resumo Semanal
        resumo_tab = self.tabview.add("Resumo Semanal")
        self.resumo_text = ctk.CTkTextbox(resumo_tab, height=150, width=600, corner_radius=10)
        self.resumo_text.pack(pady=10)
        self.update_resumo()

        # Aba Próximos Jogos
        jogos_tab = self.tabview.add("Próximos Jogos")
        self.jogos_text = ctk.CTkTextbox(jogos_tab, height=150, width=600, corner_radius=10)
        self.jogos_text.pack(pady=10)
        self.update_jogos()

        # Aba Cotações
        cotacoes_tab = self.tabview.add("Cotações")
        self.cotacoes_text = ctk.CTkTextbox(cotacoes_tab, height=150, width=600, corner_radius=10)
        self.cotacoes_text.pack(pady=10)
        self.update_cotacoes()

    def update_resumo(self):
        try:
            response = requests.get(f"http://localhost:8000/resumo_semanal/{self.app.usuario_id}")
            response.raise_for_status()
            data = response.json()
            texto = f"Resumo Semanal:\n"
            texto += f"Receitas: R${data['total_receitas']:.2f}\n"
            texto += f"Despesas: R${data['total_despesas']:.2f}\n"
            texto += f"Apostas Ganhas: R${data['total_apostas_ganhas']:.2f}\n"
            texto += f"Apostas Perdidas: R${data['total_apostas_perdidas']:.2f}\n"
            self.resumo_text.delete("1.0", "end")
            self.resumo_text.insert("end", texto)
        except Exception as e:
            self.resumo_text.delete("1.0", "end")
            self.resumo_text.insert("end", f"Erro ao carregar resumo: {e}")

    def update_jogos(self):
        try:
            response = requests.get("http://localhost:8000/jogos_esports/")
            response.raise_for_status()
            jogos = response.json()
            texto = "Próximos Jogos:\n"
            for jogo in jogos:
                texto += f"{jogo['torneio']}: {jogo['jogo']} ({jogo['data']})\n"
            self.jogos_text.delete("1.0", "end")
            self.jogos_text.insert("end", texto)
        except Exception as e:
            self.jogos_text.delete("1.0", "end")
            self.jogos_text.insert("end", f"Erro ao carregar jogos: {e}")

    def update_cotacoes(self):
        try:
            response = requests.get("http://localhost:8000/cotacoes/")
            response.raise_for_status()
            data = response.json()
            texto = "Cotações:\n"
            texto += f"USD/BRL: {data['moedas']['USD_BRL']:.2f}\n"
            texto += f"USD/EUR: {data['moedas']['USD_EUR']:.2f}\n"
            texto += f"USD/JPY: {data['moedas']['USD_JPY']:.2f}\n"
            texto += f"IBOVESPA: {data['bolsas']['^BVSP']:.2f}\n"
            texto += f"S&P 500: {data['bolsas']['^GSPC']:.2f}\n"
            texto += f"NASDAQ: {data['bolsas']['^IXIC']:.2f}\n"
            self.cotacoes_text.delete("1.0", "end")
            self.cotacoes_text.insert("end", texto)
        except Exception as e:
            self.cotacoes_text.delete("1.0", "end")
            self.cotacoes_text.insert("end", f"Erro ao carregar cotações: {e}")