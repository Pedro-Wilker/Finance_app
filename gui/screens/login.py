import customtkinter as ctk
import requests

class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=15)
        self.app = app
        self.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Título
        ctk.CTkLabel(self, text="Login", font=("Roboto", 24, "bold")).pack(pady=20)

        # Campos
        ctk.CTkLabel(self, text="Email", font=("Roboto", 16)).pack(pady=5)
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email", width=400, height=40, corner_radius=10)
        self.email_entry.pack(pady=10)
        ctk.CTkLabel(self, text="Senha", font=("Roboto", 16)).pack(pady=5)
        self.senha_entry = ctk.CTkEntry(self, placeholder_text="Senha", show="*", width=400, height=40, corner_radius=10)
        self.senha_entry.pack(pady=10)

        # Botões
        ctk.CTkButton(self, text="Entrar", command=self.autenticar, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=15)
        ctk.CTkButton(self, text="Cadastrar", command=self.app.show_cadastro_screen, width=200, height=40, corner_radius=10, font=("Roboto", 16)).pack(pady=10)

        # Mensagem
        self.message_label = ctk.CTkLabel(self, text="", font=("Roboto", 14))
        self.message_label.pack(pady=5)

    def autenticar(self):
        email = self.email_entry.get()
        senha = self.senha_entry.get()
        try:
            response = requests.post("http://localhost:8000/login/", json={"email": email, "senha": senha})
            response.raise_for_status()
            data = response.json()
            self.app.usuario_id = data["usuario_id"]
            self.app.nome_usuario = data["nome"]
            self.message_label.configure(text=f"Bem-vindo, {self.app.nome_usuario}!", text_color="green")
            self.app.show_main_screen()
        except requests.exceptions.RequestException as e:
            self.message_label.configure(text=f"Erro: {str(e)}", text_color="red")