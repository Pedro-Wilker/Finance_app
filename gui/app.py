import customtkinter as ctk
from gui.navigation import NavigationBar
from gui.screens.login import LoginScreen
from gui.screens.cadastro import CadastroScreen
from gui.screens.home import HomeScreen
from gui.screens.transacao import TransacaoScreen
from gui.screens.custos_fixos import CustosFixosScreen
from gui.screens.apostas import ApostasScreen
from gui.screens.relatorio import RelatorioScreen
from gui.screens.resumo import ResumoScreen
from gui.screens.investimentos import InvestimentosScreen

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestão de Finanças Pessoais")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.root.minsize(1000, 600)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.usuario_id = None
        self.nome_usuario = None
        self.current_screen = None
        self.nav_bar = None
        self.show_login_screen()

    def clear_screen(self):
        if self.current_screen:
            self.current_screen.destroy()
        if self.nav_bar:
            self.nav_bar.destroy()

    def show_login_screen(self):
        self.clear_screen()
        self.current_screen = LoginScreen(self.root, self)

    def show_cadastro_screen(self):
        self.clear_screen()
        self.current_screen = CadastroScreen(self.root, self)

    def show_main_screen(self):
        self.clear_screen()
        self.nav_bar = NavigationBar(self.root, self)
        self.nav_bar.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        self.current_screen = HomeScreen(self.root, self)

    def show_transacao_screen(self):
        self.clear_screen()
        self.nav_bar = NavigationBar(self.root, self)
        self.nav_bar.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        self.current_screen = TransacaoScreen(self.root, self)

    def show_custos_fixos_screen(self):
        self.clear_screen()
        self.nav_bar = NavigationBar(self.root, self)
        self.nav_bar.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        self.current_screen = CustosFixosScreen(self.root, self)

    def show_apostas_screen(self):
        self.clear_screen()
        self.nav_bar = NavigationBar(self.root, self)
        self.nav_bar.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        self.current_screen = ApostasScreen(self.root, self)

    def show_relatorio_screen(self):
        self.clear_screen()
        self.nav_bar = NavigationBar(self.root, self)
        self.nav_bar.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        self.current_screen = RelatorioScreen(self.root, self)

    def show_resumo_screen(self):
        self.clear_screen()
        self.nav_bar = NavigationBar(self.root, self)
        self.nav_bar.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        self.current_screen = ResumoScreen(self.root, self)

    def show_investimentos_screen(self):
        self.clear_screen()
        self.nav_bar = NavigationBar(self.root, self)
        self.nav_bar.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        self.current_screen = InvestimentosScreen(self.root, self)