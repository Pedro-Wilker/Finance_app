import customtkinter as ctk
import requests

class CadastroScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=15)
        self.app = app
        self.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.etapa = 1
        self.show_etapa1()

    def show_etapa1(self):
        for widget in self.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self, text="Cadastro - Etapa 1", font=("Roboto", 24, "bold")).pack(pady=20)
        ctk.CTkLabel(self, text="Nome", font=("Roboto", 16)).pack(pady=5)
        self.nome_entry = ctk.CTkEntry(self, placeholder_text="Nome", width=400, height=40, corner_radius=10)
        self.nome_entry.pack(pady=10)
        ctk.CTkLabel(self, text="Idade", font=("Roboto", 16)).pack(pady=5)
        self.idade_entry = ctk.CTkEntry(self, placeholder_text="Idade", width=400, height=40, corner_radius=10)
        self.idade_entry.pack(pady=10)
        ctk.CTkLabel(self, text="Email", font=("Roboto", 16)).pack(pady=5)
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email", width=400, height=40, corner_radius=10)
        self.email_entry.pack(pady=10)
        ctk.CTkLabel(self, text="Senha", font=("Roboto", 16)).pack(pady=5)
        self.senha_entry = ctk.CTkEntry(self, placeholder_text="Senha", show="*", width=400, height=40, corner_radius=10)
        self.senha_entry.pack(pady=10)
        ctk.CTkButton(self, text="Próximo", command=self.show_etapa2, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=15)
        self.message_label = ctk.CTkLabel(self, text="", font=("Roboto", 14))
        self.message_label.pack(pady=5)

    def show_etapa2(self):
        nome = self.nome_entry.get().strip()
        idade = self.idade_entry.get().strip()
        email = self.email_entry.get().strip()
        senha = self.senha_entry.get().strip()

        if not all([nome, idade, email, senha]):
            self.message_label.configure(text="Erro: Preencha todos os campos.", text_color="red")
            return
        if "@" not in email or "." not in email:
            self.message_label.configure(text="Erro: Email inválido.", text_color="red")
            return
        try:
            self.idade = int(idade)
            if self.idade <= 0:
                self.message_label.configure(text="Erro: Idade deve ser maior que zero.", text_color="red")
                return
        except ValueError:
            self.message_label.configure(text="Erro: Idade deve ser um número inteiro.", text_color="red")
            return

        self.nome = nome
        self.email = email
        self.senha = senha

        for widget in self.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self, text="Cadastro - Etapa 2", font=("Roboto", 24, "bold")).pack(pady=20)
        ctk.CTkLabel(self, text="Número", font=("Roboto", 16)).pack(pady=5)
        self.numero_entry = ctk.CTkEntry(self, placeholder_text="Número", width=400, height=40, corner_radius=10)
        self.numero_entry.pack(pady=10)
        ctk.CTkLabel(self, text="Salário", font=("Roboto", 16)).pack(pady=5)
        self.salario_entry = ctk.CTkEntry(self, placeholder_text="Salário", width=400, height=40, corner_radius=10)
        self.salario_entry.pack(pady=10)
        ctk.CTkLabel(self, text="Profissão", font=("Roboto", 16)).pack(pady=5)
        self.profissao_entry = ctk.CTkEntry(self, placeholder_text="Profissão", width=400, height=40, corner_radius=10)
        self.profissao_entry.pack(pady=10)
        ctk.CTkButton(self, text="Finalizar", command=self.finalizar_cadastro, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=15)
        self.message_label = ctk.CTkLabel(self, text="", font=("Roboto", 14))
        self.message_label.pack(pady=5)

    def finalizar_cadastro(self):
        numero = self.numero_entry.get().strip() or None
        salario = self.salario_entry.get().strip() or None
        profissao = self.profissao_entry.get().strip() or None

        if salario:
            try:
                salario = float(salario)
                if salario < 0:
                    self.message_label.configure(text="Erro: Salário não pode ser negativo.", text_color="red")
                    return
            except ValueError:
                self.message_label.configure(text="Erro: Salário deve ser um número.", text_color="red")
                return

        try:
            response = requests.post("http://localhost:8000/usuarios/", json={
                "nome": self.nome, "idade": self.idade, "email": self.email, "senha": self.senha,
                "numero": numero, "salario": salario, "profissao": profissao
            })
            response.raise_for_status()
            data = response.json()
            self.app.usuario_id = data["id"]
            self.app.nome_usuario = self.nome
            self.message_label.configure(text="Cadastro concluído com sucesso!", text_color="green")
            self.app.show_main_screen()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 422:
                error_detail = e.response.json()
                self.message_label.configure(text=f"Erro 422: {error_detail}", text_color="red")
            elif e.response.status_code == 400:
                self.message_label.configure(text=f"Erro: {e.response.json()['detail']}", text_color="red")
            else:
                self.message_label.configure(text=f"Erro: {str(e)}", text_color="red")
        except requests.exceptions.RequestException as e:
            self.message_label.configure(text=f"Erro de conexão: {str(e)}", text_color="red")