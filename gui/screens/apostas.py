import customtkinter as ctk
from datetime import date
from PIL import Image
import requests

class ApostasScreen(ctk.CTkScrollableFrame):
    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=15)
        self.app = app
        self.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.grid_columnconfigure(0, weight=1)

        # Título
        ctk.CTkLabel(self, text="Apostas eSports", font=("Roboto", 24, "bold")).pack(pady=20)

        # Navegação por jogos
        self.game_nav = ctk.CTkFrame(self, fg_color="transparent")
        self.game_nav.pack(pady=10)
        games = [
            ("LoL", "assets/lol.png", lambda: self.update_jogos("lol")),
            ("Valorant", "assets/valorant.png", lambda: self.update_jogos("valorant")),
            ("CS", "assets/cs.png", lambda: self.update_jogos("cs"))
        ]
        for i, (text, icon_path, command) in enumerate(games):
            icon = ctk.CTkImage(Image.open(icon_path), size=(30, 30))
            btn = ctk.CTkButton(
                self.game_nav, text="", image=icon, command=command,
                width=60, height=60, corner_radius=15, fg_color="#3B3B3B",
                hover_color="#4CAF50"
            )
            btn.grid(row=0, column=i, padx=5, pady=5)
            ctk.CTkLabel(self.game_nav, text=text, font=("Roboto", 12)).grid(row=1, column=i, pady=2)

        # Lista de jogos
        self.jogos_text = ctk.CTkTextbox(self, height=150, width=600, corner_radius=10)
        self.jogos_text.pack(pady=10)
        self.update_jogos("lol")

        # Formulário de aposta
        self.valor_aposta_entry = ctk.CTkEntry(self, placeholder_text="Valor", width=400, height=40, corner_radius=10)
        self.valor_aposta_entry.pack(pady=10)
        self.jogo_var = ctk.StringVar()
        self.jogo_menu = ctk.CTkOptionMenu(self, values=["Selecione um jogo"], variable=self.jogo_var, width=400, height=40, corner_radius=10)
        self.jogo_menu.pack(pady=10)
        self.resultado_var = ctk.StringVar(value="Ganhou")
        ctk.CTkOptionMenu(self, values=["Ganhou", "Perdeu"], variable=self.resultado_var, width=400, height=40, corner_radius=10).pack(pady=10)
        data_frame = ctk.CTkFrame(self)
        data_frame.pack(pady=5)
        self.dia_var = ctk.StringVar(value=str(date.today().day))
        self.mes_var = ctk.StringVar(value=str(date.today().month))
        self.ano_var = ctk.StringVar(value=str(date.today().year))
        dias = [str(i) for i in range(1, 32)]
        meses = [str(i) for i in range(1, 13)]
        anos = [str(i) for i in range(2020, 2031)]
        ctk.CTkOptionMenu(data_frame, values=dias, variable=self.dia_var, width=100, height=40, corner_radius=10).pack(side="left", padx=5)
        ctk.CTkOptionMenu(data_frame, values=meses, variable=self.mes_var, width=100, height=40, corner_radius=10).pack(side="left", padx=5)
        ctk.CTkOptionMenu(data_frame, values=anos, variable=self.ano_var, width=100, height=40, corner_radius=10).pack(side="left", padx=5)
        ctk.CTkButton(self, text="Adicionar Aposta", command=self.add_aposta, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)

        # Lista de apostas
        ctk.CTkLabel(self, text="Apostas", font=("Roboto", 16)).pack(pady=10)
        self.apostas_text = ctk.CTkTextbox(self, height=200, width=600, corner_radius=10)
        self.apostas_text.pack(pady=10)
        self.update_apostas()

        # Botão voltar
        ctk.CTkButton(self, text="Voltar", command=self.app.show_main_screen, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)

    def update_jogos(self, game_type):
        try:
            response = requests.get("http://localhost:8000/jogos_esports/")
            response.raise_for_status()
            jogos = [j for j in response.json() if game_type.lower() in j["torneio"].lower() or game_type.lower() in j["jogo"].lower()]
            self.jogo_menu.configure(values=[j["jogo"] for j in jogos])
            self.jogo_var.set(jogos[0]["jogo"] if jogos else "Selecione um jogo")
            texto = f"Jogos {game_type}:\n"
            for jogo in jogos:
                texto += f"{jogo['torneio']}: {jogo['jogo']} ({jogo['data']})\n"
            self.jogos_text.delete("1.0", "end")
            self.jogos_text.insert("end", texto)
        except Exception as e:
            self.jogos_text.delete("1.0", "end")
            self.jogos_text.insert("end", f"Erro ao carregar jogos: {e}")

    def add_aposta(self):
        try:
            jogo = self.jogo_var.get()
            valor_apostado = float(self.valor_aposta_entry.get())
            resultado = self.resultado_var.get()
            data = date(int(self.ano_var.get()), int(self.mes_var.get()), int(self.dia_var.get()))
            response = requests.post("http://localhost:8000/apostas/", json={
                "jogo": jogo, "valor_apostado": valor_apostado, "resultado": resultado,
                "data": data.isoformat(), "usuario_id": self.app.usuario_id
            })
            response.raise_for_status()
            self.update_apostas()
            ctk.CTkLabel(self, text="Aposta adicionada com sucesso!", text_color="green", font=("Roboto", 14)).pack(pady=5)
            self.valor_aposta_entry.delete(0, "end")
            self.dia_var.set(str(date.today().day))
            self.mes_var.set(str(date.today().month))
            self.ano_var.set(str(date.today().year))
        except Exception as e:
            ctk.CTkLabel(self, text=f"Erro ao adicionar aposta: {e}", text_color="red", font=("Roboto", 14)).pack(pady=5)

    def update_apostas(self):
        try:
            response = requests.get(f"http://localhost:8000/apostas/{self.app.usuario_id}")
            response.raise_for_status()
            apostas = response.json()
            self.apostas_text.delete("1.0", "end")
            for a in apostas:
                self.apostas_text.insert("end", f"ID: {a['id']} | Jogo: {a['jogo']} | Valor: {a['valor_apostado']} | Resultado: {a['resultado']} | Data: {a['data']}\n")
        except Exception as e:
            self.apostas_text.delete("1.0", "end")
            self.apostas_text.insert("end", f"Erro ao carregar apostas: {e}")