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
        
        # Aguarda a janela ser criada antes de dar foco
        self.after(100, self.focus_force)