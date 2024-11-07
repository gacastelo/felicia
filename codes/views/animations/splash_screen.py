import customtkinter as ctk
from PIL import Image, ImageTk
import pygame
import os
import logging
from utils.sound_manager import SoundManager

class SplashScreen(ctk.CTkToplevel):
    def __init__(self, master, width=None, height=None):
        super().__init__(master)
        self.sound_manager = SoundManager()
        
        # Configurações de tamanho
        self.width = width or 500
        self.height = height or 300
        
        # Obtém o caminho base do aplicativo principal
        if hasattr(master, '_get_base_path'):
            self.base_path = master._get_base_path()
        else:
            self.base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Carrega a imagem usando o caminho correto
        try:
            image_path = os.path.join(self.base_path, 'assets', 'felichia_logo.png')
            self.logo_image = Image.open(image_path)
            # Resto do código...
        except Exception as e:
            logging.error(f"Erro ao carregar logo: {e}")
            # Tratamento de erro...
        
        # Configurações da janela de splash
        self.overrideredirect(True)  # Remove a barra de título
        self.lift()  # Traz a janela para frente
        self.attributes('-topmost', True)  # Mantém no topo
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 400
        window_height = 500
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Cor de fundo
        self.configure(fg_color="#1A1A1A")
        
        # Canvas para a imagem
        self.canvas = ctk.CTkCanvas(self, width=window_width, height=window_height,
                                    bg="#1A1A1A", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Calcula o tamanho da imagem baseado na resolução
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Define o tamanho máximo da imagem como uma porcentagem da tela
        image_width = int(screen_width * 0.25)  # 25% da largura da tela
        image_height = int(screen_height * 0.3)  # 30% da altura da tela

        # Mantém a proporção da imagem original
        original_ratio = 348/322  # proporção original (largura/altura)
        new_ratio = image_width/image_height

        if new_ratio > original_ratio:
            # Ajusta largura baseada na altura
            image_width = int(image_height * original_ratio)
        else:
            # Ajusta altura baseada na largura
            image_height = int(image_width / original_ratio)

        # Redimensiona a imagem
        img = self.logo_image.resize((image_width, image_height), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(img)
        self.canvas.create_image(window_width // 2, window_height // 2, image=self.photo)
        
        # Inicia o som de fundo
        self.play_sound()
        
        # Adiciona protocolo de fechamento
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Força a atualização da janela
        self.update()
    
    def play_sound(self):
        """Toca o som de inicialização"""
        try:
            success = self.sound_manager.play_sound('startup.wav')
            if not success:
                logging.error("Falha ao tocar o som do splash")
        except Exception as e:
            logging.error(f"Erro no play_sound do splash: {e}")
    
    def _on_closing(self):
        """Limpa os recursos do pygame antes de fechar"""
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except:
            pass
        finally:
            self.destroy()