import customtkinter as ctk

class BaseView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        # Remove a borda do frame definindo a cor de borda como None
        self.configure(fg_color="#242424", border_width=0)
        self.pack(fill="both", expand=True)
        
        # Configura o tamanho mínimo antes de tentar fullscreen
        self.master.minsize(800, 600)
        
        # Obtém as dimensões da tela
        largura_tela = self.master.winfo_screenwidth()
        altura_tela = self.master.winfo_screenheight()
        
        # Configura o tamanho máximo como o tamanho da tela
        self.master.maxsize(largura_tela, altura_tela)
        
        # Primeiro maximiza a janela
        self.master.state('zoomed')
        
        # Adiciona os binds de teclado
        self.master.bind("<F11>", self._alternar_tela_cheia)
        self.master.bind("<Escape>", self._sair_tela_cheia)
        
        # Variável para controlar o estado do fullscreen
        self.fullscreen = False
        
        # Agenda a configuração do fullscreen para depois que a janela estiver pronta
        self.after(200, self._configurar_tela_cheia)
    
    def _configurar_tela_cheia(self):
        try:
            # Garante que a janela está maximizada antes de tentar fullscreen
            if self.master.state() != 'zoomed':
                self.master.state('zoomed')
            
            # Aplica o fullscreen
            self.master.attributes("-fullscreen", True)
            self.fullscreen = True
            
        except Exception as e:
            print(f"Erro ao configurar tela cheia: {e}")
            # Se falhar o fullscreen, pelo menos mantém maximizado
            self.master.state('zoomed')
    
    def _alternar_tela_cheia(self, event=None):
        """Alterna entre modo tela cheia e normal"""
        self.fullscreen = not self.fullscreen
        self.master.attributes("-fullscreen", self.fullscreen)
        return "break"  # Impede que o evento se propague
    
    def _sair_tela_cheia(self, event=None):
        """Sai do modo tela cheia"""
        if self.fullscreen:
            self.fullscreen = False
            self.master.attributes("-fullscreen", False)
        return "break"  # Impede que o evento se propague