import customtkinter as ctk

class BaseSenhaPopup(ctk.CTkToplevel):
    def __init__(self, master, titulo="", largura=600, altura=500):
        super().__init__(master)
        
        # Obtém o fator de escala baseado no tamanho da fonte
        self.escala = master.master.configuracoes.get("tamanho_fonte", 13) / 13
        
        # Ajusta as dimensões baseado na escala
        largura_ajustada = int(largura * self.escala)
        altura_ajustada = int(altura * self.escala)
        
        # Configurações básicas
        self.title(titulo)
        self.geometry(f"{largura_ajustada}x{altura_ajustada}")
        
        # Força um tamanho mínimo
        self.minsize(largura_ajustada, altura_ajustada)
        
        # Centraliza a janela
        self.update_idletasks()
        x = (self.winfo_screenwidth() - largura_ajustada) // 2
        y = (self.winfo_screenheight() - altura_ajustada) // 2
        self.geometry(f"{largura_ajustada}x{altura_ajustada}+{x}+{y}")
        
        # Configurações adicionais
        self.transient(master)
        self.grab_set()
        
        # Impede redimensionamento
        self.resizable(False, False)
        
        # Configura o protocolo de fechamento
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        
        # Configura a cor da barra de título
        self._configurar_tema()
        
        # Mantém o popup sempre no topo
        self.lift()
        
        # Aguarda a janela ser criada antes de dar foco
        self.after(100, self.focus_force)
    
    def _configurar_tema(self):
        # Obtém o tema atual
        tema_atual = ctk.get_appearance_mode()
        
        if tema_atual == "Dark":
            cor_fundo = "#1a1a1a"
            cor_texto = "white"
        else:
            cor_fundo = "#f0f0f0"
            cor_texto = "black"
        
        # Configura as cores da janela
        self.configure(fg_color=cor_fundo)
        
        # Configuração da barra de título no Windows
        if self.winfo_exists():
            try:
                from ctypes import windll, byref, sizeof, c_int
                
                HWND = windll.user32.GetParent(self.winfo_id())
                DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                DWMWA_CAPTION_COLOR = 35
                
                # Configura o modo escuro/claro
                valor_modo = 1 if tema_atual == "Dark" else 0
                windll.dwmapi.DwmSetWindowAttribute(
                    HWND,
                    DWMWA_USE_IMMERSIVE_DARK_MODE,
                    byref(c_int(valor_modo)),
                    sizeof(c_int)
                )
                
                # Define a cor da barra de título
                cor_rgb = int("1a1a1a" if tema_atual == "Dark" else "f0f0f0", 16)
                windll.dwmapi.DwmSetWindowAttribute(
                    HWND,
                    DWMWA_CAPTION_COLOR,
                    byref(c_int(cor_rgb)),
                    sizeof(c_int)
                )
            except:
                pass
    
    def destroy(self):
        self.grab_release()
        super().destroy()