import customtkinter as ctk
from datetime import date
import requests

class TransacaoScreen(ctk.CTkScrollableFrame):
    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=15)
        self.app = app
        self.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.grid_columnconfigure(0, weight=1)

        # Título
        ctk.CTkLabel(self, text="Nova Transação", font=("Roboto", 24, "bold")).pack(pady=20)

        # Formulário
        self.valor_entry = ctk.CTkEntry(self, placeholder_text="Valor", width=400, height=40, corner_radius=10)
        self.valor_entry.pack(pady=10)
        self.descricao_entry = ctk.CTkEntry(self, placeholder_text="Descrição", width=400, height=40, corner_radius=10)
        self.descricao_entry.pack(pady=10)
        ctk.CTkLabel(self, text="Data", font=("Roboto", 16)).pack(pady=5)
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
        self.categoria_var = ctk.StringVar()
        self.categoria_menu = ctk.CTkOptionMenu(self, values=["Carregando..."], width=400, height=40, corner_radius=10)
        self.categoria_menu.pack(pady=10)
        ctk.CTkButton(self, text="Adicionar Transação", command=self.add_transacao, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)
        self.update_categorias()

        # Exclusão
        ctk.CTkLabel(self, text="Excluir Transação", font=("Roboto", 16)).pack(pady=10)
        self.delete_id_entry = ctk.CTkEntry(self, placeholder_text="ID da Transação", width=400, height=40, corner_radius=10)
        self.delete_id_entry.pack(pady=10)
        ctk.CTkButton(self, text="Excluir", command=self.delete_transacao, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)

        # Lista de transações
        ctk.CTkLabel(self, text="Transações", font=("Roboto", 16)).pack(pady=10)
        self.transacoes_text = ctk.CTkTextbox(self, height=200, width=600, corner_radius=10)
        self.transacoes_text.pack(pady=10)
        self.update_transacoes()

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

    def add_transacao(self):
        try:
            valor = float(self.valor_entry.get())
            descricao = self.descricao_entry.get()
            data = date(int(self.ano_var.get()), int(self.mes_var.get()), int(self.dia_var.get()))
            categoria_nome = self.categoria_menu.get().split(" (")[0]
            categoria_id = self.categorias[self.categoria_menu.get()]
            response = requests.post("http://localhost:8000/transacoes/", json={
                "valor": valor, "descricao": descricao, "data": data.isoformat(),
                "categoria_id": categoria_id, "usuario_id": self.app.usuario_id
            })
            response.raise_for_status()
            self.update_transacoes()
            self.message_label.configure(text="Transação adicionada com sucesso!", text_color="green")
            self.valor_entry.delete(0, "end")
            self.descricao_entry.delete(0, "end")
            self.dia_var.set(str(date.today().day))
            self.mes_var.set(str(date.today().month))
            self.ano_var.set(str(date.today().year))
        except ValueError:
            self.message_label.configure(text="Erro: Valor ou data inválidos.", text_color="red")
        except requests.exceptions.RequestException as e:
            self.message_label.configure(text=f"Erro ao adicionar transação: {str(e)}", text_color="red")

    def delete_transacao(self):
        try:
            transacao_id = int(self.delete_id_entry.get())
            response = requests.delete(f"http://localhost:8000/transacoes/{transacao_id}")
            response.raise_for_status()
            self.update_transacoes()
            self.message_label.configure(text="Transação excluída com sucesso!", text_color="green")
            self.delete_id_entry.delete(0, "end")
        except ValueError:
            self.message_label.configure(text="Erro: ID inválido.", text_color="red")
        except requests.exceptions.RequestException as e:
            self.message_label.configure(text=f"Erro ao excluir transação: {str(e)}", text_color="red")

    def update_transacoes(self):
        try:
            response = requests.get(f"http://localhost:8000/transacoes/{self.app.usuario_id}")
            response.raise_for_status()
            transacoes = response.json()
            self.transacoes_text.delete("1.0", "end")
            for t in transacoes:
                self.transacoes_text.insert("end", f"ID: {t['id']} | Valor: {t['valor']} | Descrição: {t['descricao']} | Data: {t['data']} | Categoria: {t['categoria']} ({t['tipo']})\n")
        except requests.exceptions.RequestException as e:
            self.transacoes_text.delete("1.0", "end")
            self.transacoes_text.insert("end", f"Erro ao carregar transações: {str(e)}")