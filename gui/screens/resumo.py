import customtkinter as ctk
import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ResumoScreen(ctk.CTkScrollableFrame):
    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=15)
        self.app = app
        self.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.grid_columnconfigure(0, weight=1)

        # Título
        ctk.CTkLabel(self, text="Resumo Total do Mês", font=("Roboto", 24, "bold")).pack(pady=20)

        # Formulário
        ctk.CTkLabel(self, text="Mês (MM)", font=("Roboto", 16)).pack(pady=5)
        self.mes_entry = ctk.CTkEntry(self, placeholder_text="Mês", width=100, height=40, corner_radius=10)
        self.mes_entry.pack(pady=10)
        ctk.CTkLabel(self, text="Ano (YYYY)", font=("Roboto", 16)).pack(pady=5)
        self.ano_entry = ctk.CTkEntry(self, placeholder_text="Ano", width=100, height=40, corner_radius=10)
        self.ano_entry.pack(pady=10)
        ctk.CTkButton(self, text="Gerar Resumo", command=self.gerar_resumo, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)

        # Resumo
        self.resumo_text = ctk.CTkTextbox(self, height=200, width=600, corner_radius=10)
        self.resumo_text.pack(pady=10)

        # Gráfico
        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.pack(pady=10, fill="both", expand=True)

        # Botão voltar
        ctk.CTkButton(self, text="Voltar", command=self.app.show_main_screen, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)

        # Mensagem
        self.message_label = ctk.CTkLabel(self, text="", font=("Roboto", 14))
        self.message_label.pack(pady=5)

    def gerar_resumo(self):
        try:
            mes = int(self.mes_entry.get())
            ano = int(self.ano_entry.get())

            # Obter dados
            response_trans = requests.get(f"http://localhost:8000/transacoes/{self.app.usuario_id}")
            response_trans.raise_for_status()
            transacoes = [t for t in response_trans.json() if t["data"].startswith(f"{ano}-{mes:02d}")]

            response_fixos = requests.get(f"http://localhost:8000/custos_ganhos_fixos/{self.app.usuario_id}")
            response_fixos.raise_for_status()
            fixos = response_fixos.json()

            response_apostas = requests.get(f"http://localhost:8000/apostas/{self.app.usuario_id}")
            response_apostas.raise_for_status()
            apostas = [a for a in response_apostas.json() if a["data"].startswith(f"{ano}-{mes:02d}")]

            # Calcular totais
            total_receitas = 0
            total_despesas = 0
            total_apostas_ganhas = 0
            total_apostas_perdidas = 0

            # Transações
            transacao_totals = {"Receita": 0, "Despesa": 0}
            for t in transacoes:
                if t["tipo"] == "Receita":
                    transacao_totals["Receita"] += t["valor"]
                    total_receitas += t["valor"]
                else:
                    transacao_totals["Despesa"] += t["valor"]
                    total_despesas += t["valor"]

            # Custos/Ganhos Fixos
            fixo_totals = {"Receita": 0, "Despesa": 0}
            for f in fixos:
                if f["tipo"] == "Receita":
                    fixo_totals["Receita"] += f["valor"]
                    total_receitas += f["valor"]
                else:
                    fixo_totals["Despesa"] += f["valor"]
                    total_despesas += f["valor"]

            # Apostas
            aposta_totals = {"Ganhou": 0, "Perdeu": 0}
            for a in apostas:
                if a["resultado"] == "Ganhou":
                    aposta_totals["Ganhou"] += a["valor_apostado"]
                    total_apostas_ganhas += a["valor_apostado"]
                    total_receitas += a["valor_apostado"]
                else:
                    aposta_totals["Perdeu"] += a["valor_apostado"]
                    total_apostas_perdidas += a["valor_apostado"]
                    total_despesas += a["valor_apostado"]

            # Exibir resumo
            texto = f"Resumo Total - {mes:02d}/{ano}\n\n"
            texto += "Transações:\n"
            texto += f"Receitas: R${transacao_totals['Receita']:.2f}\n"
            texto += f"Despesas: R${transacao_totals['Despesa']:.2f}\n"
            texto += "\nCustos e Ganhos Fixos:\n"
            texto += f"Receitas: R${fixo_totals['Receita']:.2f}\n"
            texto += f"Despesas: R${fixo_totals['Despesa']:.2f}\n"
            texto += "\nApostas:\n"
            texto += f"Ganhou: R${aposta_totals['Ganhou']:.2f}\n"
            texto += f"Perdeu: R${aposta_totals['Perdeu']:.2f}\n"
            texto += f"\nTotal de Receitas: R${total_receitas:.2f}\n"
            texto += f"Total de Despesas: R${total_despesas:.2f}\n"
            texto += f"Saldo: R${total_receitas - total_despesas:.2f}\n"
            self.resumo_text.delete("1.0", "end")
            self.resumo_text.insert("end", texto)

            # Gráfico
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()
            data = [
                ("Receitas Transações", transacao_totals["Receita"]),
                ("Despesas Transações", transacao_totals["Despesa"]),
                ("Receitas Fixas", fixo_totals["Receita"]),
                ("Despesas Fixas", fixo_totals["Despesa"]),
                ("Apostas Ganhas", aposta_totals["Ganhou"]),
                ("Apostas Perdidas", aposta_totals["Perdeu"])
            ]
            df = pd.DataFrame(data, columns=["tipo", "valor"])
            fig, ax = plt.subplots(figsize=(8, 5))
            df.plot(kind="bar", x="tipo", y="valor", ax=ax, title="Resumo por Tipo")
            ax.set_xlabel("Tipo")
            ax.set_ylabel("Valor (R$)")
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10)

            self.message_label.configure(text="Resumo gerado com sucesso!", text_color="green")
        except ValueError:
            self.message_label.configure(text="Erro: Mês ou ano inválidos.", text_color="red")
        except requests.exceptions.RequestException as e:
            self.message_label.configure(text=f"Erro ao gerar resumo: {str(e)}", text_color="red")