import customtkinter as ctk
import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class RelatorioScreen(ctk.CTkScrollableFrame):
    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=15)
        self.app = app
        self.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.grid_columnconfigure(0, weight=1)

        # Título
        ctk.CTkLabel(self, text="Relatório Mensal", font=("Roboto", 24, "bold")).pack(pady=20)

        # Formulário
        ctk.CTkLabel(self, text="Mês (MM)", font=("Roboto", 16)).pack(pady=5)
        self.mes_entry = ctk.CTkEntry(self, placeholder_text="Mês", width=100, height=40, corner_radius=10)
        self.mes_entry.pack(pady=10)
        ctk.CTkLabel(self, text="Ano (YYYY)", font=("Roboto", 16)).pack(pady=5)
        self.ano_entry = ctk.CTkEntry(self, placeholder_text="Ano", width=100, height=40, corner_radius=10)
        self.ano_entry.pack(pady=10)
        ctk.CTkButton(self, text="Gerar Relatório", command=self.gerar_relatorio, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)

        # Listas
        ctk.CTkLabel(self, text="Transações", font=("Roboto", 16)).pack(pady=10)
        self.transacoes_text = ctk.CTkTextbox(self, height=200, width=600, corner_radius=10)
        self.transacoes_text.pack(pady=10)
        ctk.CTkLabel(self, text="Custos e Ganhos Fixos", font=("Roboto", 16)).pack(pady=10)
        self.fixos_text = ctk.CTkTextbox(self, height=200, width=600, corner_radius=10)
        self.fixos_text.pack(pady=10)

        # Saldo
        self.saldo_label = ctk.CTkLabel(self, text="", font=("Roboto", 16, "bold"))
        self.saldo_label.pack(pady=10)

        # Gráfico
        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.pack(pady=10, fill="both", expand=True)

        # Botão voltar
        ctk.CTkButton(self, text="Voltar", command=self.app.show_main_screen, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)

        # Mensagem
        self.message_label = ctk.CTkLabel(self, text="", font=("Roboto", 14))
        self.message_label.pack(pady=5)

    def gerar_relatorio(self):
        try:
            mes = int(self.mes_entry.get())
            ano = int(self.ano_entry.get())

            # Transações
            response_trans = requests.get(f"http://localhost:8000/transacoes/{self.app.usuario_id}")
            response_trans.raise_for_status()
            transacoes = [t for t in response_trans.json() if t["data"].startswith(f"{ano}-{mes:02d}")]
            self.transacoes_text.delete("1.0", "end")
            total_receitas = 0
            total_despesas = 0
            for t in transacoes:
                self.transacoes_text.insert("end", f"Categoria: {t['categoria']} ({t['tipo']}) | Valor: R${t['valor']:.2f} | Descrição: {t['descricao']} | Data: {t['data']}\n")
                if t["tipo"] == "Receita":
                    total_receitas += t["valor"]
                else:
                    total_despesas += t["valor"]

            # Custos/Ganhos Fixos
            response_fixos = requests.get(f"http://localhost:8000/custos_ganhos_fixos/{self.app.usuario_id}")
            response_fixos.raise_for_status()
            fixos = response_fixos.json()
            self.fixos_text.delete("1.0", "end")
            for f in fixos:
                self.fixos_text.insert("end", f"ID: {f['id']} | Valor: {f['valor']} | Descrição: {f['descricao']} | Dia: {f['dia']} | Categoria: {f['categoria']} | Tipo: {f['tipo']}\n")
                if f["tipo"] == "Receita":
                    total_receitas += f["valor"]
                else:
                    total_despesas += f["valor"]

            # Saldo
            saldo = total_receitas - total_despesas
            self.saldo_label.configure(text=f"Saldo: R${saldo:.2f}")

            # Gráfico
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()
            df = pd.DataFrame(
                [(t["categoria"], t["tipo"], t["valor"]) for t in transacoes] +
                [(f["categoria"], f["tipo"], f["valor"]) for f in fixos],
                columns=["categoria", "tipo", "valor"]
            )
            df_despesas = df[df["tipo"] == "Despesa"]
            df_receitas = df[df["tipo"] == "Receita"]
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
            df_despesas.groupby("categoria")["valor"].sum().plot(kind="pie", ax=ax1, title="Despesas por Categoria")
            df_receitas.groupby("categoria")["valor"].sum().plot(kind="pie", ax=ax2, title="Receitas por Categoria")
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10)

            self.message_label.configure(text="Relatório gerado com sucesso!", text_color="green")
        except ValueError:
            self.message_label.configure(text="Erro: Mês ou ano inválidos.", text_color="red")
        except requests.exceptions.RequestException as e:
            self.message_label.configure(text=f"Erro ao gerar relatório: {str(e)}", text_color="red")