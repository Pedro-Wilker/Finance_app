import customtkinter as ctk
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db.database import Database
import smtplib
from email.mime.text import MIMEText

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestão de Finanças Pessoais")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")  # Tema moderno
        self.root.minsize(800, 600)  # Tamanho mínimo da janela
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
            print(f"Bem-vindo, {nome}!")
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

        # Formulário de Transações
        ctk.CTkLabel(self.frame, text="Nova Transação", font=("Roboto", 20, "bold")).pack(pady=10)
        self.valor_entry = ctk.CTkEntry(self.frame, placeholder_text="Valor", width=400, height=40, corner_radius=10)
        self.valor_entry.pack(pady=10)
        self.descricao_entry = ctk.CTkEntry(self.frame, placeholder_text="Descrição", width=400, height=40, corner_radius=10)
        self.descricao_entry.pack(pady=10)

        # Seletores de Data
        ctk.CTkLabel(self.frame, text="Data", font=("Roboto", 16)).pack(pady=5)
        data_frame = ctk.CTkFrame(self.frame)
        data_frame.pack(pady=5)
        self.dia_var = ctk.StringVar(value="1")
        self.mes_var = ctk.StringVar(value="1")
        self.ano_var = ctk.StringVar(value="2025")
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

        # Exclusão de Transações
        ctk.CTkLabel(self.frame, text="Excluir Transação", font=("Roboto", 16)).pack(pady=10)
        self.delete_id_entry = ctk.CTkEntry(self.frame, placeholder_text="ID da Transação", width=400, height=40, corner_radius=10)
        self.delete_id_entry.pack(pady=10)
        ctk.CTkButton(self.frame, text="Excluir", command=self.delete_transacao, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)

        # Tabela de Transações
        ctk.CTkLabel(self.frame, text="Transações", font=("Roboto", 20, "bold")).pack(pady=10)
        self.transacoes_text = ctk.CTkTextbox(self.frame, height=300, width=600, corner_radius=10)
        self.transacoes_text.pack(pady=10)
        self.update_transacoes()

        # Relatório e Gráfico
        buttons_frame = ctk.CTkFrame(self.frame)
        buttons_frame.pack(pady=10)
        ctk.CTkButton(buttons_frame, text="Exibir Gráfico", command=self.show_grafico, width=150, height=40, corner_radius=10, font=("Roboto", 16)).pack(side="left", padx=10)
        ctk.CTkButton(buttons_frame, text="Gerar Relatório Mensal", command=self.gerar_relatorio, width=150, height=40, corner_radius=10, font=("Roboto", 16)).pack(side="left", padx=10)
        ctk.CTkLabel(buttons_frame, text="Mês (MM)", font=("Roboto", 14)).pack(side="left", padx=10)
        self.mes_entry = ctk.CTkEntry(buttons_frame, placeholder_text="Mês", width=100, height=40, corner_radius=10)
        self.mes_entry.pack(side="left", padx=10)
        ctk.CTkLabel(buttons_frame, text="Ano (YYYY)", font=("Roboto", 14)).pack(side="left", padx=10)
        self.ano_entry = ctk.CTkEntry(buttons_frame, placeholder_text="Ano", width=100, height=40, corner_radius=10)
        self.ano_entry.pack(side="left", padx=10)

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
            self.valor_entry.delete(0, "end")
            self.descricao_entry.delete(0, "end")
            self.dia_var.set("1")
            self.mes_var.set("1")
            self.ano_var.set("2025")
            ctk.CTkLabel(self.frame, text="Transação adicionada com sucesso!", text_color="green", font=("Roboto", 14)).pack(pady=5)
        except ValueError as e:
            ctk.CTkLabel(self.frame, text="Erro: Valor ou data inválidos.", text_color="red", font=("Roboto", 14)).pack(pady=5)
        except Exception as e:
            ctk.CTkLabel(self.frame, text=f"Erro ao adicionar transação: {e}", text_color="red", font=("Roboto", 14)).pack(pady=5)

    def delete_transacao(self):
        try:
            transacao_id = int(self.delete_id_entry.get())
            self.db.delete_transacao(transacao_id)
            self.update_transacoes()
            self.delete_id_entry.delete(0, "end")
            ctk.CTkLabel(self.frame, text="Transação excluída com sucesso!", text_color="green", font=("Roboto", 14)).pack(pady=5)
        except ValueError as e:
            ctk.CTkLabel(self.frame, text="Erro: ID inválido.", text_color="red", font=("Roboto", 14)).pack(pady=5)
        except Exception as e:
            ctk.CTkLabel(self.frame, text=f"Erro ao excluir transação: {e}", text_color="red", font=("Roboto", 14)).pack(pady=5)

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

        fig, ax = plt.subplots(figsize=(8, 6))
        df_despesas.groupby("categoria")["valor"].sum().plot(kind="pie", ax=ax, title="Despesas por Categoria")
        canvas = FigureCanvasTkAgg(fig, master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

    def gerar_relatorio(self):
        try:
            mes = int(self.mes_entry.get())
            ano = int(self.ano_entry.get())
            relatorio = self.db.get_relatorio_mensal(self.usuario_id, ano, mes)
            relatorio_texto = f"Relatório Mensal - {mes:02d}/{ano}\n\n"
            total_receitas = 0
            total_despesas = 0
            for nome, tipo, total in relatorio:
                relatorio_texto += f"{tipo} - {nome}: R${total:.2f}\n"
                if tipo == "Receita":
                    total_receitas += total
                else:
                    total_despesas += total
            saldo = total_receitas - total_despesas
            relatorio_texto += f"\nTotal de Receitas: R${total_receitas:.2f}\n"
            relatorio_texto += f"Total de Despesas: R${total_despesas:.2f}\n"
            relatorio_texto += f"Saldo: R${saldo:.2f}\n"

            relatorio_window = ctk.CTkToplevel(self.root)
            relatorio_window.title(f"Relatório {mes:02d}/{ano}")
            relatorio_window.minsize(600, 400)
            ctk.CTkLabel(relatorio_window, text=relatorio_texto, font=("Roboto", 14), justify="left").pack(pady=20, padx=20)

            self.db.cursor.execute("SELECT email FROM usuarios WHERE id = %s", (self.usuario_id,))
            email = self.db.cursor.fetchone()[0]
            self.enviar_email(email, relatorio_texto, mes, ano)
        except ValueError as e:
            ctk.CTkLabel(self.frame, text="Erro: Mês ou ano inválidos.", text_color="red", font=("Roboto", 14)).pack(pady=5)
        except Exception as e:
            ctk.CTkLabel(self.frame, text=f"Erro ao gerar relatório: {e}", text_color="red", font=("Roboto", 14)).pack(pady=5)

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