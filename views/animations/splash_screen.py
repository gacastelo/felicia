import customtkinter as ctk
from PIL import Image, ImageTk
import pygame

class SplashScreen(ctk.CTkToplevel):
    def __init__(self, image_path, sound_path):
        super().__init__()
        
        # Configurações da janela de splash
        self.overrideredirect(True)  # Remove a barra de título
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 400
        window_height = 500
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Cor de fundo
        self.bg_color = "#1A1A1A"
        self.configure(bg=self.bg_color)
        
        # Canvas para a imagem
        self.canvas = ctk.CTkCanvas(self, width=window_width, height=window_height,
                                    bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Carrega a imagem e redimensiona
        img = Image.open(image_path)
        img = img.resize((300, 300), Image.LANCZOS)  # Usa LANCZOS em vez de ANTIALIAS
        self.photo = ImageTk.PhotoImage(img)
        self.canvas.create_image(window_width // 2, window_height // 2, image=self.photo)
        
        # Inicia o som de fundo
        pygame.mixer.init()
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
        
        # Fecha o splash após 3 segundos
        self.after(3000, self.destroy)

def show_splash():
    splash = SplashScreen("felichia_logo.png", "splash_sound.mp3")
    splash.wait_window()  # Espera o splash fechar antes de continuar