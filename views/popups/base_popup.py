import customtkinter as ctk

class BasePopup(ctk.CTkToplevel):
    def __init__(self, master, titulo, largura=500, altura=550):
        super().__init__(master)
        
        # Configurações básicas
        self.title(titulo)
        self.geometry(f"{largura}x{altura}")
        
        # Força um tamanho mínimo
        self.minsize(largura, altura)
        
        # Centraliza a janela
        self.update_idletasks()
        x = (self.winfo_screenwidth() - largura) // 2
        y = (self.winfo_screenheight() - altura) // 2
        self.geometry(f"{largura}x{altura}+{x}+{y}")
        
        # Configurações adicionais
        self.transient(master)
        self.grab_set()
        
        # Impede redimensionamento
        self.resizable(False, False)
        
        # Configura o protocolo de fechamento
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        
        # Configura a cor da barra de título
        self._configurar_tema()
        
        # Aguarda a janela ser criada antes de dar foco
        self.after(100, self.focus_force)
    
    def _configurar_tema(self):
        # Obtém o tema atual
        tema_atual = ctk.get_appearance_mode()
        
        if tema_atual == "Dark":
            # Cores para tema escuro
            cor_fundo = "#1a1a1a"  # Cor escura para o fundo
            cor_texto = "white"    # Texto branco
        else:
            # Cores para tema claro
            cor_fundo = "#f0f0f0"  # Cor clara para o fundo
            cor_texto = "black"    # Texto preto
        
        # Configura as cores da janela
        self.configure(fg_color=cor_fundo)
        
        # No Windows, configura a cor da barra de título
        if self.winfo_exists():
            try:
                from ctypes import windll, byref, sizeof, c_int
                
                HWND = windll.user32.GetParent(self.winfo_id())
                
                # Constantes do Windows
                DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                DWMWA_CAPTION_COLOR = 35
                
                # Ativa o modo escuro na barra de título
                if tema_atual == "Dark":
                    windll.dwmapi.DwmSetWindowAttribute(
                        HWND,
                        DWMWA_USE_IMMERSIVE_DARK_MODE,
                        byref(c_int(1)),
                        sizeof(c_int)
                    )
                    # Define a cor da barra de título
                    cor_rgb = int("1a1a1a", 16)  # Converte hex para int
                else:
                    windll.dwmapi.DwmSetWindowAttribute(
                        HWND,
                        DWMWA_USE_IMMERSIVE_DARK_MODE,
                        byref(c_int(0)),
                        sizeof(c_int)
                    )
                    # Define a cor da barra de título
                    cor_rgb = int("f0f0f0", 16)  # Converte hex para int
                
                # Aplica a cor da barra de título
                windll.dwmapi.DwmSetWindowAttribute(
                    HWND,
                    DWMWA_CAPTION_COLOR,
                    byref(c_int(cor_rgb)),
                    sizeof(c_int)
                )
            except:
                pass  # Ignora erros se não estiver no Windows ou se falhar