import customtkinter as ctk
from datetime import date
import requests

class CustosFixosScreen(ctk.CTkScrollableFrame):
    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=15)
        self.app = app
        self.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.grid_columnconfigure(0, weight=1)

        # Título
        ctk.CTkLabel(self, text="Custos e Ganhos Fixos", font=("Roboto", 24, "bold")).pack(pady=20)

        # Formulário
        self.valor_entry = ctk.CTkEntry(self, placeholder_text="Valor", width=400, height=40, corner_radius=10)
        self.valor_entry.pack(pady=10)
        self.descricao_entry = ctk.CTkEntry(self, placeholder_text="Descrição", width=400, height=40, corner_radius=10)
        self.descricao_entry.pack(pady=10)
        ctk.CTkLabel(self, text="Dia do Mês", font=("Roboto", 16)).pack(pady=5)
        self.dia_var = ctk.StringVar(value=str(date.today().day))
        dias = [str(i) for i in range(1, 32)]
        ctk.CTkOptionMenu(self, values=dias, variable=self.dia_var, width=400, height=40, corner_radius=10).pack(pady=10)
        self.tipo_var = ctk.StringVar(value="Receita")
        ctk.CTkOptionMenu(self, values=["Receita", "Despesa"], variable=self.tipo_var, width=400, height=40, corner_radius=10).pack(pady=10)
        self.categoria_var = ctk.StringVar()
        self.categoria_menu = ctk.CTkOptionMenu(self, values=["Carregando..."], width=400, height=40, corner_radius=10)
        self.categoria_menu.pack(pady=10)
        ctk.CTkButton(self, text="Adicionar Custo/Ganho Fixo", command=self.add_custo_ganho_fixo, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)
        self.update_categorias()

        # Lista de custos/ganhos fixos
        ctk.CTkLabel(self, text="Custos e Ganhos Fixos", font=("Roboto", 16)).pack(pady=10)
        self.fixos_text = ctk.CTkTextbox(self, height=200, width=600, corner_radius=10)
        self.fixos_text.pack(pady=10)
        self.update_fixos()

        # Botão voltar
        ctk.CTkButton(self, text="Voltar", command=self.app.show_main_screen, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)

        # Mensagem
        self.message_label = ctk.CTkLabel(self, text="", font=("Roboto", 14))
        self.message_label.pack(pady=5)

    def update_categorias(self):
        try:
            response = requests.get("http://localhost:8000/categorias/")
            response.raise_for_status()
            categorias = response.json()
            self.categoria_menu.configure(values=[f"{c['nome']} ({c['tipo']})" for c in categorias])
            self.categoria_var.set(categorias[0]["nome"] if categorias else "Selecione uma categoria")
            self.categorias = {f"{c['nome']} ({c['tipo']})": c["id"] for c in categorias}
        except requests.exceptions.RequestException as e:
            self.message_label.configure(text=f"Erro ao carregar categorias: {str(e)}", text_color="red")

    def add_custo_ganho_fixo(self):
        try:
            valor = float(self.valor_entry.get())
            descricao = self.descricao_entry.get()
            dia = int(self.dia_var.get())
            tipo = self.tipo_var.get()
            categoria_nome = self.categoria_menu.get().split(" (")[0]
            categoria_id = self.categorias[self.categoria_menu.get()]
            response = requests.post("http://localhost:8000/custos_ganhos_fixos/", json={
                "valor": valor, "descricao": descricao, "categoria_id": categoria_id,
                "usuario_id": self.app.usuario_id, "tipo": tipo, "dia": dia
            })
            response.raise_for_status()
            self.update_fixos()
            self.message_label.configure(text="Custo/Ganho fixo adicionado com sucesso!", text_color="green")
            self.valor_entry.delete(0, "end")
            self.descricao_entry.delete(0, "end")
            self.dia_var.set(str(date.today().day))
        except ValueError:
            self.message_label.configure(text="Erro: Valor ou dia inválidos.", text_color="red")
        except requests.exceptions.RequestException as e:
            self.message_label.configure(text=f"Erro ao adicionar: {str(e)}", text_color="red")

    def update_fixos(self):
        try:
            response = requests.get(f"http://localhost:8000/custos_ganhos_fixos/{self.app.usuario_id}")
            response.raise_for_status()
            fixos = response.json()
            self.fixos_text.delete("1.0", "end")
            for f in fixos:
                self.fixos_text.insert("end", f"ID: {f['id']} | Valor: {f['valor']} | Descrição: {f['descricao']} | Dia: {f['dia']} | Categoria: {f['categoria']} | Tipo: {f['tipo']}\n")
        except requests.exceptions.RequestException as e:
            self.fixos_text.delete("1.0", "end")
            self.fixos_text.insert("end", f"Erro ao carregar custos/ganhos fixos: {str(e)}")