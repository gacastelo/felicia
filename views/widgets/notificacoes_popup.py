import customtkinter as ctk
from utils.notificacao_service import NotificacaoService

class NotificacoesPopup(ctk.CTkToplevel):
    def __init__(self, master, usuario_id):
        super().__init__(master)
        self.usuario_id = usuario_id
        self.title("Notificações")
        
        # Configurações da janela
        self.geometry("400x500")
        self.resizable(False, False)
        
        # Frame principal para as notificações
        self.frame_notificacoes = ctk.CTkScrollableFrame(self, width=380, height=450)
        self.frame_notificacoes.pack(padx=10, pady=10)
        
        # Carregar notificações
        self.carregar_notificacoes()
    
    def carregar_notificacoes(self):
        # Limpar notificações antigas
        for widget in self.frame_notificacoes.winfo_children():
            widget.destroy()
            
        # Buscar notificações do usuário
        notificacao_service = NotificacaoService()
        notificacoes = notificacao_service.buscar_notificacoes(self.usuario_id)
        
        # Criar widgets para cada notificação
        for notificacao in notificacoes:
            frame_notif = ctk.CTkFrame(self.frame_notificacoes)
            frame_notif.pack(fill="x", padx=5, pady=5)
            
            # Título da notificação
            ctk.CTkLabel(
                frame_notif,
                text=notificacao.titulo,
                font=("Arial", 12, "bold")
            ).pack(anchor="w", padx=5, pady=(5,0))
            
            # Mensagem da notificação
            ctk.CTkLabel(
                frame_notif,
                text=notificacao.mensagem,
                wraplength=350
            ).pack(anchor="w", padx=5, pady=(0,5))
            
            # Data da notificação
            ctk.CTkLabel(
                frame_notif,
                text=notificacao.data.strftime("%d/%m/%Y %H:%M"),
                font=("Arial", 10),
                text_color="gray"
            ).pack(anchor="e", padx=5, pady=(0,5))