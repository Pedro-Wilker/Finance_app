import customtkinter as ctk
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db.database import Database

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestão de Finanças Pessoais")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.db = Database()
        self.usuario_id = self.db.insert_usuario("Usuário Padrão")
        self.setup_categorias()
        self.setup_gui()

    def setup_categorias(self):
        categorias = [
            ("Salário", "Receita"), ("Investimentos", "Receita"),
            ("Alimentação", "Despesa"), ("Transporte", "Despesa"),
            ("Lazer", "Despesa"), ("Contas", "Despesa")
        ]
        for nome, tipo in categorias:
            self.db.insert_categoria(nome, tipo)

    def setup_gui(self):
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(pady=20, padx=20, fill="both")

        # Formulário de Transações
        self.valor_entry = ctk.CTkEntry(self.frame, placeholder_text="Valor")
        self.valor_entry.grid(row=0, column=0, padx=5, pady=5)
        self.descricao_entry = ctk.CTkEntry(self.frame, placeholder_text="Descrição")
        self.descricao_entry.grid(row=0, column=1, padx=5, pady=5)
        self.data_entry = ctk.CTkEntry(self.frame, placeholder_text="Data (YYYY-MM-DD)")
        self.data_entry.grid(row=0, column=2, padx=5, pady=5)

        self.categoria_var = ctk.StringVar()
        categorias = self.db.get_categorias()
        self.categoria_menu = ctk.CTkOptionMenu(self.frame, values=[f"{c[1]} ({c[2]})" for c in categorias])
        self.categoria_menu.grid(row=0, column=3, padx=5, pady=5)

        self.add_button = ctk.CTkButton(self.frame, text="Adicionar", command=self.add_transacao)
        self.add_button.grid(row=0, column=4, padx=5, pady=5)

        # Tabela de Transações
        self.transacoes_label = ctk.CTkLabel(self.frame, text="Transações")
        self.transacoes_label.grid(row=1, column=0, columnspan=5, pady=10)
        self.transacoes_text = ctk.CTkTextbox(self.frame, height=200, width=600)
        self.transacoes_text.grid(row=2, column=0, columnspan=5, pady=5)
        self.update_transacoes()

        # Gráfico
        self.grafico_button = ctk.CTkButton(self.frame, text="Exibir Gráfico", command=self.show_grafico)
        self.grafico_button.grid(row=3, column=0, columnspan=5, pady=10)

    def add_transacao(self):
        try:
            valor = float(self.valor_entry.get())
            descricao = self.descricao_entry.get()
            data = datetime.strptime(self.data_entry.get(), "%Y-%m-%d").date()
            categoria_nome = self.categoria_menu.get().split(" (")[0]
            categorias = self.db.get_categorias()
            categoria_id = next(c[0] for c in categorias if c[1] == categoria_nome)
            self.db.insert_transacao(valor, descricao, data, categoria_id, self.usuario_id)
            self.update_transacoes()
            self.valor_entry.delete(0, "end")
            self.descricao_entry.delete(0, "end")
            self.data_entry.delete(0, "end")
        except ValueError as e:
            print("Erro ao adicionar transação: Valor ou data inválidos.", e)
        except Exception as e:
            print("Erro ao adicionar transação:", e)

    def update_transacoes(self):
        self.transacoes_text.delete("1.0", "end")
        transacoes = self.db.get_transacoes(self.usuario_id)
        for t in transacoes:
            self.transacoes_text.insert("end", f"ID: {t[0]} | Valor: {t[1]} | Descrição: {t[2]} | Data: {t[3]} | Categoria: {t[4]} ({t[5]})\n")

    def show_grafico(self):
        transacoes = self.db.get_transacoes(self.usuario_id)
        df = pd.DataFrame(transacoes, columns=["id", "valor", "descricao", "data", "categoria", "tipo"])
        df_despesas = df[df["tipo"] == "Despesa"]
        df_receitas = df[df["tipo"] == "Receita"]
        
        fig, ax = plt.subplots()
        df_despesas.groupby("categoria")["valor"].sum().plot(kind="pie", ax=ax, title="Despesas por Categoria")
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=4, column=0, columnspan=5, pady=10)

    def __del__(self):
        self.db.close()