import customtkinter as ctk
from datetime import datetime, date
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db.database import Database
import smtplib
from email.mime.text import MIMEText
import requests

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestão de Finanças Pessoais")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.root.minsize(800, 600)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.db = Database()
        self.usuario_id = None
        self.show_login_screen()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_frame()
        self.frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.frame, text="Login", font=("Roboto", 24, "bold")).pack(pady=20)
        ctk.CTkLabel(self.frame, text="Email", font=("Roboto", 16)).pack(pady=5)
        self.email_entry = ctk.CTkEntry(self.frame, placeholder_text="Email", width=400, height=40, corner_radius=10)
        self.email_entry.pack(pady=10)
        ctk.CTkLabel(self.frame, text="Senha", font=("Roboto", 16)).pack(pady=5)
        self.senha_entry = ctk.CTkEntry(self.frame, placeholder_text="Senha", show="*", width=400, height=40, corner_radius=10)
        self.senha_entry.pack(pady=10)

        ctk.CTkButton(self.frame, text="Entrar", command=self.autenticar, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=15)
        ctk.CTkButton(self.frame, text="Cadastrar", command=self.show_cadastro_screen1, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)

    def autenticar(self):
        email = self.email_entry.get()
        senha = self.senha_entry.get()
        usuario = self.db.autenticar_usuario(email, senha)
        if usuario:
            self.usuario_id, nome = usuario
            ctk.CTkLabel(self.frame, text=f"Bem-vindo, {nome}!", text_color="green", font=("Roboto", 14)).pack(pady=5)
            self.setup_categorias()
            self.show_main_screen()
        else:
            ctk.CTkLabel(self.frame, text="Erro: Email ou senha incorretos.", text_color="red", font=("Roboto", 14)).pack(pady=5)

    def show_cadastro_screen1(self):
        self.clear_frame()
        self.frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.frame, text="Cadastro - Etapa 1", font=("Roboto", 24, "bold")).pack(pady=20)
        ctk.CTkLabel(self.frame, text="Nome", font=("Roboto", 16)).pack(pady=5)
        self.nome_entry = ctk.CTkEntry(self.frame, placeholder_text="Nome", width=400, height=40, corner_radius=10)
        self.nome_entry.pack(pady=10)
        ctk.CTkLabel(self.frame, text="Idade", font=("Roboto", 16)).pack(pady=5)
        self.idade_entry = ctk.CTkEntry(self.frame, placeholder_text="Idade", width=400, height=40, corner_radius=10)
        self.idade_entry.pack(pady=10)
        ctk.CTkLabel(self.frame, text="Email", font=("Roboto", 16)).pack(pady=5)
        self.email_entry = ctk.CTkEntry(self.frame, placeholder_text="Email", width=400, height=40, corner_radius=10)
        self.email_entry.pack(pady=10)
        ctk.CTkLabel(self.frame, text="Senha", font=("Roboto", 16)).pack(pady=5)
        self.senha_entry = ctk.CTkEntry(self.frame, placeholder_text="Senha", show="*", width=400, height=40, corner_radius=10)
        self.senha_entry.pack(pady=10)

        ctk.CTkButton(self.frame, text="Próximo", command=self.show_cadastro_screen2, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=15)

    def show_cadastro_screen2(self):
        try:
            nome = self.nome_entry.get()
            idade = int(self.idade_entry.get())
            email = self.email_entry.get()
            senha = self.senha_entry.get()
            self.usuario_id = self.db.insert_usuario(nome, idade, email, senha)
            self.clear_frame()
            self.frame = ctk.CTkFrame(self.root, corner_radius=15)
            self.frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
            self.frame.grid_rowconfigure(0, weight=1)
            self.frame.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(self.frame, text="Cadastro - Etapa 2", font=("Roboto", 24, "bold")).pack(pady=20)
            ctk.CTkLabel(self.frame, text="Número", font=("Roboto", 16)).pack(pady=5)
            self.numero_entry = ctk.CTkEntry(self.frame, placeholder_text="Número", width=400, height=40, corner_radius=10)
            self.numero_entry.pack(pady=10)
            ctk.CTkLabel(self.frame, text="Salário", font=("Roboto", 16)).pack(pady=5)
            self.salario_entry = ctk.CTkEntry(self.frame, placeholder_text="Salário", width=400, height=40, corner_radius=10)
            self.salario_entry.pack(pady=10)
            ctk.CTkLabel(self.frame, text="Profissão", font=("Roboto", 16)).pack(pady=5)
            self.profissao_entry = ctk.CTkEntry(self.frame, placeholder_text="Profissão", width=400, height=40, corner_radius=10)
            self.profissao_entry.pack(pady=10)

            ctk.CTkButton(self.frame, text="Finalizar", command=self.finalizar_cadastro, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=15)
        except ValueError as e:
            ctk.CTkLabel(self.frame, text="Erro: Idade deve ser um número.", text_color="red", font=("Roboto", 14)).pack(pady=5)
        except Exception as e:
            ctk.CTkLabel(self.frame, text=f"Erro ao cadastrar usuário: {e}", text_color="red", font=("Roboto", 14)).pack(pady=5)

    def finalizar_cadastro(self):
        try:
            numero = self.numero_entry.get()
            salario = float(self.salario_entry.get()) if self.salario_entry.get() else None
            profissao = self.profissao_entry.get()
            self.db.update_usuario(self.usuario_id, numero, salario, profissao)
            ctk.CTkLabel(self.frame, text="Cadastro concluído com sucesso!", text_color="green", font=("Roboto", 14)).pack(pady=5)
            self.setup_categorias()
            self.show_main_screen()
        except ValueError as e:
            ctk.CTkLabel(self.frame, text="Erro: Salário deve ser um número.", text_color="red", font=("Roboto", 14)).pack(pady=5)
        except Exception as e:
            ctk.CTkLabel(self.frame, text=f"Erro ao finalizar cadastro: {e}", text_color="red", font=("Roboto", 14)).pack(pady=5)

    def setup_categorias(self):
        categorias = [
            ("Salário", "Receita"), ("Investimentos", "Receita"),
            ("Alimentação", "Despesa"), ("Transporte", "Despesa"),
            ("Lazer", "Despesa"), ("Contas", "Despesa")
        ]
        for nome, tipo in categorias:
            self.db.insert_categoria(nome, tipo)

    def show_main_screen(self):
        self.clear_frame()
        self.frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.frame, text="Gestão de Finanças", font=("Roboto", 24, "bold")).pack(pady=20)
        ctk.CTkButton(self.frame, text="Adicionar Transação", command=self.show_transacao_screen, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)
        ctk.CTkButton(self.frame, text="Custos/Ganhos Fixos", command=self.show_custos_ganhos_fixos_screen, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)
        ctk.CTkButton(self.frame, text="Apostas eSports", command=self.show_apostas_screen, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)
        ctk.CTkButton(self.frame, text="Relatório Mensal", command=self.show_relatorio_mensal_screen, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)
        ctk.CTkButton(self.frame, text="Resumo Total", command=self.show_resumo_total_screen, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)

    def show_transacao_screen(self):
        self.clear_frame()
        self.frame = ctk.CTkScrollableFrame(self.root, corner_radius=15)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.frame, text="Nova Transação", font=("Roboto", 20, "bold")).pack(pady=10)
        self.valor_entry = ctk.CTkEntry(self.frame, placeholder_text="Valor", width=400, height=40, corner_radius=10)
        self.valor_entry.pack(pady=10)
        self.descricao_entry = ctk.CTkEntry(self.frame, placeholder_text="Descrição", width=400, height=40, corner_radius=10)
        self.descricao_entry.pack(pady=10)

        ctk.CTkLabel(self.frame, text="Data", font=("Roboto", 16)).pack(pady=5)
        data_frame = ctk.CTkFrame(self.frame)
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
        categorias = self.db.get_categorias()
        self.categoria_menu = ctk.CTkOptionMenu(self.frame, values=[f"{c[1]} ({c[2]})" for c in categorias], width=400, height=40, corner_radius=10)
        self.categoria_menu.pack(pady=10)

        ctk.CTkButton(self.frame, text="Adicionar Transação", command=self.add_transacao, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)

        ctk.CTkLabel(self.frame, text="Excluir Transação", font=("Roboto", 16)).pack(pady=10)
        self.delete_id_entry = ctk.CTkEntry(self.frame, placeholder_text="ID da Transação", width=400, height=40, corner_radius=10)
        self.delete_id_entry.pack(pady=10)
        ctk.CTkButton(self.frame, text="Excluir", command=self.delete_transacao, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)

        ctk.CTkLabel(self.frame, text="Transações", font=("Roboto", 16)).pack(pady=10)
        self.transacoes_text = ctk.CTkTextbox(self.frame, height=200, width=600, corner_radius=10)
        self.transacoes_text.pack(pady=10)
        self.update_transacoes()

        ctk.CTkButton(self.frame, text="Voltar", command=self.show_main_screen, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)

    def show_custos_ganhos_fixos_screen(self):
        self.clear_frame()
        self.frame = ctk.CTkScrollableFrame(self.root, corner_radius=15)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.frame, text="Custos e Ganhos Fixos", font=("Roboto", 20, "bold")).pack(pady=10)
        self.valor_fixo_entry = ctk.CTkEntry(self.frame, placeholder_text="Valor", width=400, height=40, corner_radius=10)
        self.valor_fixo_entry.pack(pady=10)
        self.descricao_fixa_entry = ctk.CTkEntry(self.frame, placeholder_text="Descrição", width=400, height=40, corner_radius=10)
        self.descricao_fixa_entry.pack(pady=10)

        ctk.CTkLabel(self.frame, text="Dia do Mês", font=("Roboto", 16)).pack(pady=5)
        self.dia_fixo_var = ctk.StringVar(value=str(date.today().day))
        dias = [str(i) for i in range(1, 32)]
        ctk.CTkOptionMenu(self.frame, values=dias, variable=self.dia_fixo_var, width=400, height=40, corner_radius=10).pack(pady=10)

        self.tipo_fixo_var = ctk.StringVar(value="Receita")
        ctk.CTkOptionMenu(self.frame, values=["Receita", "Despesa"], variable=self.tipo_fixo_var, width=400, height=40, corner_radius=10).pack(pady=10)

        self.categoria_fixa_var = ctk.StringVar()
        categorias = self.db.get_categorias()
        self.categoria_fixa_menu = ctk.CTkOptionMenu(self.frame, values=[f"{c[1]} ({c[2]})" for c in categorias], width=400, height=40, corner_radius=10)
        self.categoria_fixa_menu.pack(pady=10)

        ctk.CTkButton(self.frame, text="Adicionar Custo/Ganho Fixo", command=self.add_custo_ganho_fixo, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)

        ctk.CTkLabel(self.frame, text="Custos e Ganhos Fixos", font=("Roboto", 16)).pack(pady=10)
        self.fixos_text = ctk.CTkTextbox(self.frame, height=200, width=600, corner_radius=10)
        self.fixos_text.pack(pady=10)
        self.update_custos_ganhos_fixos()

        ctk.CTkButton(self.frame, text="Voltar", command=self.show_main_screen, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)

    def show_apostas_screen(self):
        self.clear_frame()
        self.frame = ctk.CTkScrollableFrame(self.root, corner_radius=15)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.frame, text="Apostas eSports", font=("Roboto", 20, "bold")).pack(pady=10)

        # Buscar jogos da API LoL eSports (fallback para lista fictícia)
        try:
            response = requests.get("http://na.lolesports.com/api/programming.json?parameters[method]=all¶meters[week]=1¶meters[tournament]=102¶meters[expand_matches]=1")
            jogos_data = response.json()
            jogos = [f"{match['contestants']['blue']['name']} vs {match['contestants']['red']['name']}" for match in jogos_data[0]['matches'].values()]
        except:
            jogos = ["T1 vs Gen.G", "SKT vs DRX", "Fnatic vs G2 Esports"]  # Fallback

        ctk.CTkLabel(self.frame, text="Jogo", font=("Roboto", 16)).pack(pady=5)
        self.jogo_var = ctk.StringVar()
        ctk.CTkOptionMenu(self.frame, values=jogos, variable=self.jogo_var, width=400, height=40, corner_radius=10).pack(pady=10)

        ctk.CTkLabel(self.frame, text="Valor Apostado", font=("Roboto", 16)).pack(pady=5)
        self.valor_aposta_entry = ctk.CTkEntry(self.frame, placeholder_text="Valor", width=400, height=40, corner_radius=10)
        self.valor_aposta_entry.pack(pady=10)

        ctk.CTkLabel(self.frame, text="Resultado", font=("Roboto", 16)).pack(pady=5)
        self.resultado_var = ctk.StringVar(value="Ganhou")
        ctk.CTkOptionMenu(self.frame, values=["Ganhou", "Perdeu"], variable=self.resultado_var, width=400, height=40, corner_radius=10).pack(pady=10)

        ctk.CTkLabel(self.frame, text="Data", font=("Roboto", 16)).pack(pady=5)
        data_frame = ctk.CTkFrame(self.frame)
        data_frame.pack(pady=5)
        self.dia_aposta_var = ctk.StringVar(value=str(date.today().day))
        self.mes_aposta_var = ctk.StringVar(value=str(date.today().month))
        self.ano_aposta_var = ctk.StringVar(value=str(date.today().year))
        dias = [str(i) for i in range(1, 32)]
        meses = [str(i) for i in range(1, 13)]
        anos = [str(i) for i in range(2020, 2031)]
        ctk.CTkOptionMenu(data_frame, values=dias, variable=self.dia_aposta_var, width=100, height=40, corner_radius=10).pack(side="left", padx=5)
        ctk.CTkOptionMenu(data_frame, values=meses, variable=self.mes_aposta_var, width=100, height=40, corner_radius=10).pack(side="left", padx=5)
        ctk.CTkOptionMenu(data_frame, values=anos, variable=self.ano_aposta_var, width=100, height=40, corner_radius=10).pack(side="left", padx=5)

        ctk.CTkButton(self.frame, text="Adicionar Aposta", command=self.add_aposta, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)

        ctk.CTkLabel(self.frame, text="Apostas", font=("Roboto", 16)).pack(pady=10)
        self.apostas_text = ctk.CTkTextbox(self.frame, height=200, width=600, corner_radius=10)
        self.apostas_text.pack(pady=10)
        self.update_apostas()

        ctk.CTkButton(self.frame, text="Voltar", command=self.show_main_screen, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)

    def show_relatorio_mensal_screen(self):
        self.clear_frame()
        self.frame = ctk.CTkScrollableFrame(self.root, corner_radius=15)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.frame, text="Relatório Mensal", font=("Roboto", 20, "bold")).pack(pady=10)
        ctk.CTkLabel(self.frame, text="Mês (MM)", font=("Roboto", 16)).pack(pady=5)
        self.mes_relatorio_entry = ctk.CTkEntry(self.frame, placeholder_text="Mês", width=100, height=40, corner_radius=10)
        self.mes_relatorio_entry.pack(pady=10)
        ctk.CTkLabel(self.frame, text="Ano (YYYY)", font=("Roboto", 16)).pack(pady=5)
        self.ano_relatorio_entry = ctk.CTkEntry(self.frame, placeholder_text="Ano", width=100, height=40, corner_radius=10)
        self.ano_relatorio_entry.pack(pady=10)

        ctk.CTkButton(self.frame, text="Gerar Relatório", command=self.gerar_relatorio_mensal, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)

        ctk.CTkLabel(self.frame, text="Transações", font=("Roboto", 16)).pack(pady=10)
        self.transacoes_text = ctk.CTkTextbox(self.frame, height=200, width=600, corner_radius=10)
        self.transacoes_text.pack(pady=10)

        ctk.CTkLabel(self.frame, text="Custos e Ganhos Fixos", font=("Roboto", 16)).pack(pady=10)
        self.fixos_text = ctk.CTkTextbox(self.frame, height=200, width=600, corner_radius=10)
        self.fixos_text.pack(pady=10)

        ctk.CTkButton(self.frame, text="Voltar", command=self.show_main_screen, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)

    def show_resumo_total_screen(self):
        self.clear_frame()
        self.frame = ctk.CTkScrollableFrame(self.root, corner_radius=15)
        self.frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.frame, text="Resumo Total do Mês", font=("Roboto", 20, "bold")).pack(pady=10)
        ctk.CTkLabel(self.frame, text="Mês (MM)", font=("Roboto", 16)).pack(pady=5)
        self.mes_resumo_entry = ctk.CTkEntry(self.frame, placeholder_text="Mês", width=100, height=40, corner_radius=10)
        self.mes_resumo_entry.pack(pady=10)
        ctk.CTkLabel(self.frame, text="Ano (YYYY)", font=("Roboto", 16)).pack(pady=5)
        self.ano_resumo_entry = ctk.CTkEntry(self.frame, placeholder_text="Ano", width=100, height=40, corner_radius=10)
        self.ano_resumo_entry.pack(pady=10)

        ctk.CTkButton(self.frame, text="Gerar Resumo", command=self.gerar_resumo_total, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)

        ctk.CTkButton(self.frame, text="Voltar", command=self.show_main_screen, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)

    def add_transacao(self):
        try:
            valor = float(self.valor_entry.get())
            descricao = self.descricao_entry.get()
            dia = int(self.dia_var.get())
            mes = int(self.mes_var.get())
            ano = int(self.ano_var.get())
            data = datetime(ano, mes, dia).date()
            categoria_nome = self.categoria_menu.get().split(" (")[0]
            categorias = self.db.get_categorias()
            categoria_id = next(c[0] for c in categorias if c[1] == categoria_nome)
            self.db.insert_transacao(valor, descricao, data, categoria_id, self.usuario_id)
            self.update_transacoes()
            ctk.CTkLabel(self.frame, text="Transação adicionada com sucesso!", text_color="green", font=("Roboto", 14)).pack(pady=5)
            self.valor_entry.delete(0, "end")
            self.descricao_entry.delete(0, "end")
            self.dia_var.set(str(date.today().day))
            self.mes_var.set(str(date.today().month))
            self.ano_var.set(str(date.today().year))
        except ValueError as e:
            ctk.CTkLabel(self.frame, text="Erro: Valor ou data inválidos.", text_color="red", font=("Roboto", 14)).pack(pady=5)
        except Exception as e:
            ctk.CTkLabel(self.frame, text=f"Erro ao adicionar transação: {e}", text_color="red", font=("Roboto", 14)).pack(pady=5)

    def add_custo_ganho_fixo(self):
        try:
            valor = float(self.valor_fixo_entry.get())
            descricao = self.descricao_fixa_entry.get()
            dia = int(self.dia_fixo_var.get())
            tipo = self.tipo_fixo_var.get()
            categoria_nome = self.categoria_fixa_menu.get().split(" (")[0]
            categorias = self.db.get_categorias()
            categoria_id = next(c[0] for c in categorias if c[1] == categoria_nome)
            self.db.insert_custo_ganho_fixo(valor, descricao, categoria_id, self.usuario_id, tipo, dia)
            self.update_custos_ganhos_fixos()
            ctk.CTkLabel(self.frame, text="Custo/Ganho fixo adicionado com sucesso!", text_color="green", font=("Roboto", 14)).pack(pady=5)
            self.valor_fixo_entry.delete(0, "end")
            self.descricao_fixa_entry.delete(0, "end")
            self.dia_fixo_var.set(str(date.today().day))
        except ValueError as e:
            ctk.CTkLabel(self.frame, text="Erro: Valor ou dia inválidos.", text_color="red", font=("Roboto", 14)).pack(pady=5)
        except Exception as e:
            ctk.CTkLabel(self.frame, text=f"Erro ao adicionar custo/ganho fixo: {e}", text_color="red", font=("Roboto", 14)).pack(pady=5)

    def add_aposta(self):
        try:
            jogo = self.jogo_var.get()
            valor_apostado = float(self.valor_aposta_entry.get())
            resultado = self.resultado_var.get()
            dia = int(self.dia_aposta_var.get())
            mes = int(self.mes_aposta_var.get())
            ano = int(self.ano_aposta_var.get())
            data = datetime(ano, mes, dia).date()
            self.db.insert_aposta(jogo, valor_apostado, resultado, data, self.usuario_id)
            self.update_apostas()
            ctk.CTkLabel(self.frame, text="Aposta adicionada com sucesso!", text_color="green", font=("Roboto", 14)).pack(pady=5)
            self.valor_aposta_entry.delete(0, "end")
            self.dia_aposta_var.set(str(date.today().day))
            self.mes_aposta_var.set(str(date.today().month))
            self.ano_aposta_var.set(str(date.today().year))
        except ValueError as e:
            ctk.CTkLabel(self.frame, text="Erro: Valor ou data inválidos.", text_color="red", font=("Roboto", 14)).pack(pady=5)
        except Exception as e:
            ctk.CTkLabel(self.frame, text=f"Erro ao adicionar aposta: {e}", text_color="red", font=("Roboto", 14)).pack(pady=5)

    def delete_transacao(self):
        try:
            transacao_id = int(self.delete_id_entry.get())
            self.db.delete_transacao(transacao_id)
            self.update_transacoes()
            ctk.CTkLabel(self.frame, text="Transação excluída com sucesso!", text_color="green", font=("Roboto", 14)).pack(pady=5)
            self.delete_id_entry.delete(0, "end")
        except ValueError as e:
            ctk.CTkLabel(self.frame, text="Erro: ID inválido.", text_color="red", font=("Roboto", 14)).pack(pady=5)
        except Exception as e:
            ctk.CTkLabel(self.frame, text=f"Erro ao excluir transação: {e}", text_color="red", font=("Roboto", 14)).pack(pady=5)

    def update_custos_ganhos_fixos(self):
        self.fixos_text.delete("1.0", "end")
        fixos = self.db.get_custos_ganhos_fixos(self.usuario_id)
        for f in fixos:
            self.fixos_text.insert("end", f"ID: {f[0]} | Valor: {f[1]} | Descrição: {f[2]} | Dia: {f[3]} | Categoria: {f[4]} | Tipo: {f[5]}\n")

    def update_apostas(self):
        self.apostas_text.delete("1.0", "end")
        apostas = self.db.get_apostas(self.usuario_id)
        for a in apostas:
            self.apostas_text.insert("end", f"ID: {a[0]} | Jogo: {a[1]} | Valor Apostado: {a[2]} | Resultado: {a[3]} | Data: {a[4]}\n")

    def update_transacoes(self):
        self.transacoes_text.delete("1.0", "end")
        transacoes = self.db.get_transacoes(self.usuario_id)
        for t in transacoes:
            self.transacoes_text.insert("end", f"ID: {t[0]} | Valor: {t[1]} | Descrição: {t[2]} | Data: {t[3]} | Categoria: {t[4]} ({t[5]})\n")

    def gerar_relatorio_mensal(self):
        try:
            mes = int(self.mes_relatorio_entry.get())
            ano = int(self.ano_relatorio_entry.get())
            relatorio = self.db.get_relatorio_mensal(self.usuario_id, ano, mes)
            fixos = self.db.get_custos_ganhos_fixos(self.usuario_id)
            
            self.transacoes_text.delete("1.0", "end")
            self.fixos_text.delete("1.0", "end")
            total_receitas = 0
            total_despesas = 0

            for nome, tipo, total in relatorio:
                self.transacoes_text.insert("end", f"{tipo} - {nome}: R${total:.2f}\n")
                if tipo == "Receita":
                    total_receitas += total
                else:
                    total_despesas += total

            for f in fixos:
                self.fixos_text.insert("end", f"ID: {f[0]} | Valor: {f[1]} | Descrição: {f[2]} | Dia: {f[3]} | Categoria: {f[4]} | Tipo: {f[5]}\n")
                if f[5] == "Receita":
                    total_receitas += f[1]
                else:
                    total_despesas += f[1]

            saldo = total_receitas - total_despesas
            ctk.CTkLabel(self.frame, text=f"Saldo: R${saldo:.2f}", font=("Roboto", 16, "bold")).pack(pady=10)

            # Gráfico
            df = pd.DataFrame(relatorio + [(f[4], f[5], f[1]) for f in fixos], columns=["categoria", "tipo", "valor"])
            df_despesas = df[df["tipo"] == "Despesa"]
            df_receitas = df[df["tipo"] == "Receita"]
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
            df_despesas.groupby("categoria")["valor"].sum().plot(kind="pie", ax=ax1, title="Despesas por Categoria")
            df_receitas.groupby("categoria")["valor"].sum().plot(kind="pie", ax=ax2, title="Receitas por Categoria")
            canvas = FigureCanvasTkAgg(fig, master=self.frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10)

            # Enviar por email
            relatorio_texto = f"Relatório Mensal - {mes:02d}/{ano}\n\nTransações:\n"
            for nome, tipo, total in relatorio:
                relatorio_texto += f"{tipo} - {nome}: R${total:.2f}\n"
            relatorio_texto += "\nCustos e Ganhos Fixos:\n"
            for f in fixos:
                relatorio_texto += f"{f[5]} - {f[4]}: R${f[1]:.2f} (Dia {f[3]})\n"
            relatorio_texto += f"\nTotal de Receitas: R${total_receitas:.2f}\n"
            relatorio_texto += f"Total de Despesas: R${total_despesas:.2f}\n"
            relatorio_texto += f"Saldo: R${saldo:.2f}\n"

            self.db.cursor.execute("SELECT email FROM usuarios WHERE id = %s", (self.usuario_id,))
            email = self.db.cursor.fetchone()[0]
            self.enviar_email(email, relatorio_texto, mes, ano)
        except ValueError as e:
            ctk.CTkLabel(self.frame, text="Erro: Mês ou ano inválidos.", text_color="red", font=("Roboto", 14)).pack(pady=5)
        except Exception as e:
            ctk.CTkLabel(self.frame, text=f"Erro ao gerar relatório: {e}", text_color="red", font=("Roboto", 14)).pack(pady=5)

    def gerar_resumo_total(self):
        try:
            mes = int(self.mes_resumo_entry.get())
            ano = int(self.ano_resumo_entry.get())
            transacoes, fixos, apostas = self.db.get_resumo_mensal(self.usuario_id, ano, mes)

            relatorio_window = ctk.CTkToplevel(self.root)
            relatorio_window.title(f"Resumo Total - {mes:02d}/{ano}")
            relatorio_window.minsize(600, 400)
            relatorio_window.grid_rowconfigure(0, weight=1)
            relatorio_window.grid_columnconfigure(0, weight=1)

            frame = ctk.CTkScrollableFrame(relatorio_window, corner_radius=15)
            frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

            total_receitas = 0
            total_despesas = 0
            total_apostas_ganhas = 0
            total_apostas_perdidas = 0

            texto = f"Resumo Total - {mes:02d}/{ano}\n\nTransações:\n"
            for tipo, total in transacoes:
                texto += f"{tipo}: R${total:.2f}\n"
                if tipo == "Receita":
                    total_receitas += total
                else:
                    total_despesas += total

            texto += "\nCustos e Ganhos Fixos:\n"
            for tipo, total in fixos:
                texto += f"{tipo}: R${total:.2f}\n"
                if tipo == "Receita":
                    total_receitas += total
                else:
                    total_despesas += total

            texto += "\nApostas:\n"
            for resultado, total in apostas:
                texto += f"{resultado}: R${total:.2f}\n"
                if resultado == "Ganhou":
                    total_apostas_ganhas += total
                    total_receitas += total
                else:
                    total_apostas_perdidas += total
                    total_despesas += total

            saldo = total_receitas - total_despesas
            texto += f"\nTotal de Receitas: R${total_receitas:.2f}\n"
            texto += f"Total de Despesas: R${total_despesas:.2f}\n"
            texto += f"Saldo: R${saldo:.2f}\n"

            ctk.CTkLabel(frame, text=texto, font=("Roboto", 14), justify="left").pack(pady=20, padx=20)

            # Gráfico
            df_transacoes = pd.DataFrame(transacoes + fixos + [(r, t) for r, t in apostas], columns=["tipo", "valor"])
            fig, ax = plt.subplots(figsize=(8, 5))
            df_transacoes.groupby("tipo")["valor"].sum().plot(kind="bar", ax=ax, title="Resumo por Tipo")
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10)

            ctk.CTkButton(frame, text="Voltar", command=relatorio_window.destroy, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)

        except ValueError as e:
            ctk.CTkLabel(self.frame, text="Erro: Mês ou ano inválidos.", text_color="red", font=("Roboto", 14)).pack(pady=5)
        except Exception as e:
            ctk.CTkLabel(self.frame, text=f"Erro ao gerar resumo: {e}", text_color="red", font=("Roboto", 14)).pack(pady=5)

    def enviar_email(self, destinatario, relatorio_texto, mes, ano):
        try:
            remetente = "seu_email@example.com"  # Substitua pelo seu email
            senha = "sua_senha"  # Substitua pela senha do seu email
            msg = MIMEText(relatorio_texto)
            msg['Subject'] = f"Relatório Financeiro - {mes:02d}/{ano}"
            msg['From'] = remetente
            msg['To'] = destinatario

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(remetente, senha)
                server.sendmail(remetente, destinatario, msg.as_string())
            ctk.CTkLabel(self.frame, text="Relatório enviado por email com sucesso!", text_color="green", font=("Roboto", 14)).pack(pady=5)
        except Exception as e:
            ctk.CTkLabel(self.frame, text=f"Erro ao enviar email: {e}", text_color="red", font=("Roboto", 14)).pack(pady=5)

    def __del__(self):
        self.db.close()