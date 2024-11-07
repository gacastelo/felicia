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
import tkinter as tk
import os
from ctypes import windll
import sys
from PIL import Image
from log_utils import setup_logging

# Configuração do logging
def configurar_logging():
    try:
        # Define o diretório base para os logs
        if getattr(sys, 'frozen', False):
            # Se for executável
            base_dir = os.path.join(os.environ.get('APPDATA', ''), 'Felichia')
        else:
            # Se for desenvolvimento
            base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Cria o diretório base se não existir
        os.makedirs(base_dir, exist_ok=True)
        
        # Define e cria o diretório de logs
        log_dir = os.path.join(base_dir, 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        # Define o arquivo de log
        log_file = os.path.join(log_dir, 'felichia.log')
        
        # Configura o logging
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            encoding='utf-8'
        )
        
        # Adiciona log no console para desenvolvimento
        if not getattr(sys, 'frozen', False):
            console = logging.StreamHandler()
            console.setLevel(logging.INFO)
            formatter = logging.Formatter('%(levelname)s: %(message)s')
            console.setFormatter(formatter)
            logging.getLogger('').addHandler(console)
        
        logging.info('Logging iniciado com sucesso')
        return True
        
    except Exception as e:
        # Se falhar, tenta criar um arquivo de erro no desktop
        try:
            desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
            error_file = os.path.join(desktop, 'felichia_error.log')
            with open(error_file, 'w', encoding='utf-8') as f:
                f.write(f'Erro ao configurar logging: {str(e)}')
        except:
            pass
        return False

# Configura o logging antes de qualquer outra operação
if not configurar_logging():
    # Se falhar em configurar o logging, configura apenas para console
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s'
    )

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuração de logging
        self._configurar_logging()
        
        # Configuração de caminhos
        self.base_path = self._get_base_path()
        self.assets_path = os.path.join(self.base_path, 'assets')
        self.database_path = os.path.join(self.base_path, 'database')
        
        # Obtém o caminho absoluto para a pasta assets
        base_path = Path(__file__).parent
        icon_path = base_path / "assets" / "icones" / "felichia.ico"
        
        # Configurações iniciais da janela
        self.title("Felichia - Login")
        self.geometry("800x600")
        
        # Adiciona o ícone da aplicação
        try:
            if os.name == 'nt':  # Windows
                # Define o ícone tanto para a janela quanto para a barra de tarefas
                self.iconbitmap(default=str(icon_path))
                self.wm_iconbitmap(str(icon_path))
                
                # Força o Windows a atualizar o ícone na barra de tarefas
                windll.shell32.Shell_NotifyIconW(0x0, str(icon_path))
            else:  # Linux/Mac
                icon = tk.PhotoImage(file=str(icon_path.with_suffix('.png')))
                self.iconphoto(True, icon)
                self.wm_iconphoto(True, icon)
        except Exception as e:
            logging.error(f"Erro ao carregar ícone: {e}")
        
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

    def _get_base_path(self):
        """Retorna o caminho base correto seja executando como script ou como executável"""
        if getattr(sys, 'frozen', False):
            # Se estiver rodando como executável
            return sys._MEIPASS
        else:
            # Se estiver rodando como script Python
            return os.path.dirname(os.path.abspath(__file__))
    
    def _load_image(self, image_name):
        """Carrega uma imagem usando o caminho correto"""
        image_path = os.path.join(self.assets_path, image_name)
        try:
            return Image.open(image_path)
        except Exception as e:
            logging.error(f"Erro ao carregar imagem {image_name}: {e}")
            return None

    def show_splash(self):
        try:
            # Cria e mostra a tela de splash
            splash = SplashScreen(self)  # Remove argumentos extras se não necessários
            # ou
            # splash = SplashScreen(self, width=500, height=300)  # Se precisar especificar tamanho
            
            # Resto do código...
        except Exception as e:
            logging.error(f"Erro ao mostrar splash screen: {e}")
            # Tratamento de erro...

if __name__ == "__main__":
    app = App()
    app.withdraw()
    
    # Cria o splash screen passando a aplicação principal como master
    app.show_splash()
    
    def depois_splash():
        """Função para executar após o splash"""
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except:
            pass
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
    app.after(3000, depois_splash)
    
    # Inicia o loop principal
    app.mainloop()