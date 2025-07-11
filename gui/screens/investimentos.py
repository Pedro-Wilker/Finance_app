import customtkinter as ctk
from datetime import date
import requests

class InvestimentosScreen(ctk.CTkScrollableFrame):
    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=15)
        self.app = app
        self.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.grid_columnconfigure(0, weight=1)

        # Título
        ctk.CTkLabel(self, text="Investimentos", font=("Roboto", 24, "bold")).pack(pady=20)

        # Formulário
        self.valor_entry = ctk.CTkEntry(self, placeholder_text="Valor", width=400, height=40, corner_radius=10)
        self.valor_entry.pack(pady=10)
        self.tipo_var = ctk.StringVar(value="Ação")
        ctk.CTkOptionMenu(self, values=["Ação", "Fundo", "Criptomoeda"], variable=self.tipo_var, width=400, height=40, corner_radius=10).pack(pady=10)
        self.descricao_entry = ctk.CTkEntry(self, placeholder_text="Descrição", width=400, height=40, corner_radius=10)
        self.descricao_entry.pack(pady=10)
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
        ctk.CTkButton(self, text="Adicionar Investimento", command=self.add_investimento, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)

        # Exclusão
        ctk.CTkLabel(self, text="Excluir Investimento", font=("Roboto", 16)).pack(pady=10)
        self.delete_id_entry = ctk.CTkEntry(self, placeholder_text="ID do Investimento", width=400, height=40, corner_radius=10)
        self.delete_id_entry.pack(pady=10)
        ctk.CTkButton(self, text="Excluir", command=self.delete_investimento, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)

        # Lista de investimentos
        ctk.CTkLabel(self, text="Investimentos", font=("Roboto", 16)).pack(pady=10)
        self.investimentos_text = ctk.CTkTextbox(self, height=200, width=600, corner_radius=10)
        self.investimentos_text.pack(pady=10)
        self.update_investimentos()

        # Botão voltar
        ctk.CTkButton(self, text="Voltar", command=self.app.show_main_screen, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)

    def add_investimento(self):
        try:
            valor = float(self.valor_entry.get())
            tipo = self.tipo_var.get()
            descricao = self.descricao_entry.get()
            data = date(int(self.ano_var.get()), int(self.mes_var.get()), int(self.dia_var.get()))
            response = requests.post("http://localhost:8000/investimentos/", json={
                "valor": valor, "tipo": tipo, "descricao": descricao,
                "data": data.isoformat(), "usuario_id": self.app.usuario_id
            })
            response.raise_for_status()
            self.update_investimentos()
            ctk.CTkLabel(self, text="Investimento adicionado com sucesso!", text_color="green", font=("Roboto", 14)).pack(pady=5)
            self.valor_entry.delete(0, "end")
            self.descricao_entry.delete(0, "end")
            self.dia_var.set(str(date.today().day))
            self.mes_var.set(str(date.today().month))
            self.ano_var.set(str(date.today().year))
        except Exception as e:
            ctk.CTkLabel(self, text=f"Erro ao adicionar investimento: {e}", text_color="red", font=("Roboto", 14)).pack(pady=5)

    def delete_investimento(self):
        try:
            investimento_id = int(self.delete_id_entry.get())
            response = requests.delete(f"http://localhost:8000/investimentos/{investimento_id}")
            response.raise_for_status()
            self.update_investimentos()
            ctk.CTkLabel(self, text="Investimento excluído com sucesso!", text_color="green", font=("Roboto", 14)).pack(pady=5)
            self.delete_id_entry.delete(0, "end")
        except Exception as e:
            ctk.CTkLabel(self, text=f"Erro ao excluir investimento: {e}", text_color="red", font=("Roboto", 14)).pack(pady=5)

    def update_investimentos(self):
        try:
            response = requests.get(f"http://localhost:8000/investimentos/{self.app.usuario_id}")
            response.raise_for_status()
            investimentos = response.json()
            self.investimentos_text.delete("1.0", "end")
            for i in investimentos:
                self.investimentos_text.insert("end", f"ID: {i['id']} | Valor: {i['valor']} | Tipo: {i['tipo']} | Descrição: {i['descricao']} | Data: {i['data']}\n")
        except Exception as e:
            self.investimentos_text.delete("1.0", "end")
            self.investimentos_text.insert("end", f"Erro ao carregar investimentos: {e}")