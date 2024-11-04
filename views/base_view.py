import customtkinter as ctk

class BaseView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.fullscreen = True
        self.pack(fill="both", expand=True)
        self._configurar_tela_cheia()
        self.master.bind("<F11>", self._alternar_tela_cheia)
        self.master.bind("<Escape>", self._sair_tela_cheia)
        
    def _configurar_tela_cheia(self):
        if self.fullscreen:
            self.master.overrideredirect(False)  # Primeiro remove o override
            self.master.attributes("-fullscreen", True)  # Depois ativa fullscreen
        else:
            self.master.attributes("-fullscreen", False)
            self.master.overrideredirect(False)
            # Centraliza a janela quando sair do modo tela cheia
            largura_tela = self.master.winfo_screenwidth()
            altura_tela = self.master.winfo_screenheight()
            largura_janela = int(largura_tela * 0.8)
            altura_janela = int(altura_tela * 0.8)
            x = (largura_tela - largura_janela) // 2
            y = (altura_tela - altura_janela) // 2
            self.master.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")
    
    def _alternar_tela_cheia(self, event=None):
        self.fullscreen = not self.fullscreen
        self._configurar_tela_cheia()
    
    def _sair_tela_cheia(self, event=None):
        if self.fullscreen:
            self.fullscreen = False
            self._configurar_tela_cheia() 