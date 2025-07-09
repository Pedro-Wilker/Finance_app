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
        ctk.set_default_color_theme("blue")
        self.db = Database()
        self.usuario_id = None
        self.show_login_screen()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        self.clear_frame()
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(pady=20, padx=20, fill="both")

        ctk.CTkLabel(self.frame, text="Login").grid(row=0, column=0, columnspan=2, pady=10)
        ctk.CTkLabel(self.frame, text="Email").grid(row=1, column=0, padx=5)
        self.email_entry = ctk.CTkEntry(self.frame, placeholder_text="Email")
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)
        ctk.CTkLabel(self.frame, text="Senha").grid(row=2, column=0, padx=5)
        self.senha_entry = ctk.CTkEntry(self.frame, placeholder_text="Senha", show="*")
        self.senha_entry.grid(row=2, column=1, padx=5, pady=5)

        ctk.CTkButton(self.frame, text="Entrar", command=self.autenticar).grid(row=3, column=0, columnspan=2, pady=10)
        ctk.CTkButton(self.frame, text="Cadastrar", command=self.show_cadastro_screen1).grid(row=4, column=0, columnspan=2, pady=5)

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
            print("Erro: Email ou senha incorretos.")

    def show_cadastro_screen1(self):
        self.clear_frame()
        self.frame = ctk.CTkFrame(self.root)
        self.frame.pack(pady=20, padx=20, fill="both")

        ctk.CTkLabel(self.frame, text="Cadastro - Etapa 1").grid(row=0, column=0, columnspan=2, pady=10)
        ctk.CTkLabel(self.frame, text="Nome").grid(row=1, column=0, padx=5)
        self.nome_entry = ctk.CTkEntry(self.frame, placeholder_text="Nome")
        self.nome_entry.grid(row=1, column=1, padx=5, pady=5)
        ctk.CTkLabel(self.frame, text="Idade").grid(row=2, column=0, padx=5)
        self.idade_entry = ctk.CTkEntry(self.frame, placeholder_text="Idade")
        self.idade_entry.grid(row=2, column=1, padx=5, pady=5)
        ctk.CTkLabel(self.frame, text="Email").grid(row=3, column=0, padx=5)
        self.email_entry = ctk.CTkEntry(self.frame, placeholder_text="Email")
        self.email_entry.grid(row=3, column=1, padx=5, pady=5)
        ctk.CTkLabel(self.frame, text="Senha").grid(row=4, column=0, padx=5)
        self.senha_entry = ctk.CTkEntry(self.frame, placeholder_text="Senha", show="*")
        self.senha_entry.grid(row=4, column=1, padx=5, pady=5)

        ctk.CTkButton(self.frame, text="Próximo", command=self.show_cadastro_screen2).grid(row=5, column=0, columnspan=2, pady=10)

    def show_cadastro_screen2(self):
        try:
            nome = self.nome_entry.get()
            idade = int(self.idade_entry.get())
            email = self.email_entry.get()
            senha = self.senha_entry.get()
            self.usuario_id = self.db.insert_usuario(nome, idade, email, senha)
            self.clear_frame()
            self.frame = ctk.CTkFrame(self.root)
            self.frame.pack(pady=20, padx=20, fill="both")

            ctk.CTkLabel(self.frame, text="Cadastro - Etapa 2").grid(row=0, column=0, columnspan=2, pady=10)
            ctk.CTkLabel(self.frame, text="Número").grid(row=1, column=0, padx=5)
            self.numero_entry = ctk.CTkEntry(self.frame, placeholder_text="Número")
            self.numero_entry.grid(row=1, column=1, padx=5, pady=5)
            ctk.CTkLabel(self.frame, text="Salário").grid(row=2, column=0, padx=5)
            self.salario_entry = ctk.CTkEntry(self.frame, placeholder_text="Salário")
            self.salario_entry.grid(row=2, column=1, padx=5, pady=5)
            ctk.CTkLabel(self.frame, text="Profissão").grid(row=3, column=0, padx=5)
            self.profissao_entry = ctk.CTkEntry(self.frame, placeholder_text="Profissão")
            self.profissao_entry.grid(row=3, column=1, padx=5, pady=5)

            ctk.CTkButton(self.frame, text="Finalizar", command=self.finalizar_cadastro).grid(row=4, column=0, columnspan=2, pady=10)
        except ValueError as e:
            print("Erro: Idade deve ser um número.", e)
        except Exception as e:
            print("Erro ao cadastrar usuário:", e)

    def finalizar_cadastro(self):
        try:
            numero = self.numero_entry.get()
            salario = float(self.salario_entry.get()) if self.salario_entry.get() else None
            profissao = self.profissao_entry.get()
            self.db.update_usuario(self.usuario_id, numero, salario, profissao)
            print("Cadastro concluído com sucesso!")
            self.setup_categorias()
            self.show_main_screen()
        except ValueError as e:
            print("Erro: Salário deve ser um número.", e)
        except Exception as e:
            print("Erro ao finalizar cadastro:", e)

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

        # Exclusão de Transações
        ctk.CTkLabel(self.frame, text="ID da Transação para Excluir").grid(row=1, column=0, padx=5, pady=5)
        self.delete_id_entry = ctk.CTkEntry(self.frame, placeholder_text="ID")
        self.delete_id_entry.grid(row=1, column=1, padx=5, pady=5)
        self.delete_button = ctk.CTkButton(self.frame, text="Excluir", command=self.delete_transacao)
        self.delete_button.grid(row=1, column=2, padx=5, pady=5)

        # Tabela de Transações
        self.transacoes_label = ctk.CTkLabel(self.frame, text="Transações")
        self.transacoes_label.grid(row=2, column=0, columnspan=5, pady=10)
        self.transacoes_text = ctk.CTkTextbox(self.frame, height=200, width=600)
        self.transacoes_text.grid(row=3, column=0, columnspan=5, pady=5)
        self.update_transacoes()

        # Relatório e Gráfico
        self.grafico_button = ctk.CTkButton(self.frame, text="Exibir Gráfico", command=self.show_grafico)
        self.grafico_button.grid(row=4, column=0, padx=5, pady=5)
        self.relatorio_button = ctk.CTkButton(self.frame, text="Gerar Relatório Mensal", command=self.gerar_relatorio)
        self.relatorio_button.grid(row=4, column=1, padx=5, pady=5)
        ctk.CTkLabel(self.frame, text="Mês (MM)").grid(row=4, column=2, padx=5, pady=5)
        self.mes_entry = ctk.CTkEntry(self.frame, placeholder_text="Mês")
        self.mes_entry.grid(row=4, column=3, padx=5, pady=5)
        ctk.CTkLabel(self.frame, text="Ano (YYYY)").grid(row=4, column=4, padx=5, pady=5)
        self.ano_entry = ctk.CTkEntry(self.frame, placeholder_text="Ano")
        self.ano_entry.grid(row=4, column=5, padx=5, pady=5)

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

    def delete_transacao(self):
        try:
            transacao_id = int(self.delete_id_entry.get())
            self.db.delete_transacao(transacao_id)
            self.update_transacoes()
            self.delete_id_entry.delete(0, "end")
            print("Transação excluída com sucesso!")
        except ValueError as e:
            print("Erro: ID inválido.", e)
        except Exception as e:
            print("Erro ao excluir transação:", e)

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
        canvas.get_tk_widget().grid(row=5, column=0, columnspan=5, pady=10)

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

            # Exibir relatório
            relatorio_window = ctk.CTkToplevel(self.root)
            relatorio_window.title(f"Relatório {mes:02d}/{ano}")
            ctk.CTkLabel(relatorio_window, text=relatorio_texto).pack(pady=10, padx=10)

            # Enviar por email
            email = self.db.cursor.execute("SELECT email FROM usuarios WHERE id = %s", (self.usuario_id,))
            email = self.db.cursor.fetchone()[0]
            self.enviar_email(email, relatorio_texto, mes, ano)
        except ValueError as e:
            print("Erro: Mês ou ano inválidos.", e)
        except Exception as e:
            print("Erro ao gerar relatório:", e)

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
            print("Relatório enviado por email com sucesso!")
        except Exception as e:
            print("Erro ao enviar email:", e)

    def __del__(self):
        self.db.close()