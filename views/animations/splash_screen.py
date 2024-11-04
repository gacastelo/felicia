import customtkinter as ctk
from PIL import Image, ImageTk
import pygame

class SplashScreen(ctk.CTkToplevel):
    def __init__(self, master, image_path, sound_path):
        super().__init__(master)
        
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
        
        # Carrega a imagem e redimensiona
        img = Image.open(image_path)
        img = img.resize((348, 322), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(img)
        self.canvas.create_image(window_width // 2, window_height // 2, image=self.photo)
        
        # Inicia o som de fundo
        pygame.mixer.init()
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
        
        # Adiciona protocolo de fechamento
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Força a atualização da janela
        self.update()
    
    def _on_closing(self):
        """Limpa os recursos do pygame antes de fechar"""
        try:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
        except:
            pass
        finally:
            self.destroy()