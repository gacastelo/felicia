import customtkinter as ctk
from views.login_view import LoginView
from controllers.auth_controller import AuthController
from utils.database import Database
from utils.backup import BackupService
import logging
from pathlib import Path
from views.animations.splash_screen import SplashScreen
import pygame
import json

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuração de logging
        self._configurar_logging()
        
        # Configurações iniciais da janela
        self.title("Gerenciador de Senhas")
        self.geometry("800x600")
        # Carrega configurações salvas ou usa padrões
        self.carregar_configuracoes()
        
        # Configuração do tema padrão
        ctk.set_appearance_mode(self.configuracoes.get("tema", "dark"))
        ctk.set_default_color_theme("blue")
        
        # Aplica o tamanho da fonte salvo ou usa o padrão
        self.trocar_tamanho_fonte(self.configuracoes.get("tamanho_fonte", 13))
        
        # Inicialização do banco de dados
        self.db = Database()
        self.db.criar_tabelas()
        
        # Inicialização do controlador de autenticação
        self.auth_controller = AuthController()
        
        # Inicialização do serviço de backup
        self.backup_service = BackupService()
    
    def carregar_configuracoes(self):
        """Carrega as configurações salvas ou cria um arquivo novo com valores padrão"""
        try:
            with open('config.json', 'r') as f:
                self.configuracoes = json.load(f)
        except:
            self.configuracoes = {
                "tema": "dark",
                "tamanho_fonte": 13
            }
            self.salvar_configuracoes()
    
    def salvar_configuracoes(self):
        """Salva as configurações atuais em um arquivo"""
        try:
            with open('config.json', 'w') as f:
                json.dump(self.configuracoes, f)
        except Exception as e:
            logging.error(f"Erro ao salvar configurações: {str(e)}")
    
    def trocar_tema(self, novo_tema):
        """Troca o tema da aplicação e salva a preferência"""
        ctk.set_appearance_mode(novo_tema)
        self.configuracoes["tema"] = novo_tema
        self.salvar_configuracoes()
        logging.info(f"Tema alterado para: {novo_tema}")
    
    def trocar_tamanho_fonte(self, tamanho):
        """Atualiza o tamanho da fonte em toda a aplicação"""
        # Atualiza a fonte padrão do customtkinter
        ctk.set_widget_scaling(tamanho/13)  # 13 é o tamanho médio/padrão
        
        # Salva a preferência do usuário
        self.configuracoes["tamanho_fonte"] = tamanho
        self.salvar_configuracoes()
        logging.info(f"Tamanho da fonte alterado para: {tamanho}")

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

if __name__ == "__main__":
    app = App()
    app.withdraw()
    
    # Cria o splash screen passando a aplicação principal como master
    splash = SplashScreen(app, "./assets/felichia_logo.png", "./assets/splash_sound.mp3")
    
    def depois_splash():
        """Função para executar após o splash"""
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except:
            pass
        splash.destroy()
        app.deiconify()
        # Mostra o login apenas depois que o splash for fechado
        app.mostrar_login()
    
    def cleanup():
        """Função para limpar recursos ao fechar a aplicação"""
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except:
            pass
        finally:
            app.destroy()
    
    # Registra a função de cleanup para quando a janela for fechada
    app.protocol("WM_DELETE_WINDOW", cleanup)
    
    # Agenda o fechamento do splash e exibição da janela principal
    splash.after(3000, depois_splash)
    
    # Inicia o loop principal
    app.mainloop()