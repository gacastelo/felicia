import customtkinter as ctk

class AppView(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # ... código existente ...
        
        # Configura a cor da barra de título
        self._configurar_tema()
    
    def _configurar_tema(self):
        # Mesmo código do BasePopup
        tema_atual = ctk.get_appearance_mode()
        
        if tema_atual == "Dark":
            cor_fundo = "#1a1a1a"
            cor_texto = "white"
        else:
            cor_fundo = "#f0f0f0"
            cor_texto = "black"
        
        self.configure(fg_color=cor_fundo)
        
        if self.winfo_exists():
            try:
                from ctypes import windll, byref, sizeof, c_int
                
                HWND = windll.user32.GetParent(self.winfo_id())
                
                DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                DWMWA_CAPTION_COLOR = 35
                
                if tema_atual == "Dark":
                    windll.dwmapi.DwmSetWindowAttribute(
                        HWND,
                        DWMWA_USE_IMMERSIVE_DARK_MODE,
                        byref(c_int(1)),
                        sizeof(c_int)
                    )
                    cor_rgb = int("1a1a1a", 16)
                else:
                    windll.dwmapi.DwmSetWindowAttribute(
                        HWND,
                        DWMWA_USE_IMMERSIVE_DARK_MODE,
                        byref(c_int(0)),
                        sizeof(c_int)
                    )
                    cor_rgb = int("f0f0f0", 16)
                
                windll.dwmapi.DwmSetWindowAttribute(
                    HWND,
                    DWMWA_CAPTION_COLOR,
                    byref(c_int(cor_rgb)),
                    sizeof(c_int)
                )
            except:
                pass
    
    def trocar_tema(self, novo_tema):
        # Após trocar o tema, reconfigura as cores
        ctk.set_appearance_mode(novo_tema)
        self._configurar_tema() 