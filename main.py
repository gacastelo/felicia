import customtkinter as ctk
from views.login_view import LoginView
from controllers.auth_controller import AuthController
from utils.database import Database
from utils.backup import BackupService
import logging
from pathlib import Path

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuração de logging
        self._configurar_logging()
        
        # Configurações iniciais da janela
        self.title("Gerenciador de Senhas")
        self.geometry("800x600")
        
        # Configuração do tema padrão
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Inicialização do banco de dados
        self.db = Database()
        self.db.criar_tabelas()
        
        # Inicialização do controlador de autenticação
        self.auth_controller = AuthController()
        
        # Inicialização do serviço de backup
        self.backup_service = BackupService()
        
        # Carrega a tela de login
        self.mostrar_login()
    
    def _configurar_logging(self):
        """Configura o sistema de logging"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            filename=log_dir / "app.log",
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def mostrar_login(self):
        # Limpa a tela atual
        for widget in self.winfo_children():
            widget.destroy()
        
        # Carrega a tela de login
        LoginView(self)
    
    def trocar_tema(self, novo_tema):
        ctk.set_appearance_mode(novo_tema)
        logging.info(f"Tema alterado para: {novo_tema}")

if __name__ == "__main__":
    app = App()
    app.mainloop() 