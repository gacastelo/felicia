import customtkinter as ctk
from utils.notificacao_service import NotificacaoService
from views.widgets.notificacoes_popup import NotificacoesPopup

class NotificacaoWidget(ctk.CTkFrame):
    def __init__(self, master, usuario_id):
        super().__init__(master)
        self.usuario_id = usuario_id
        self.notificacao_service = NotificacaoService()
        
        # Botão de notificações
        self.btn_notificacoes = ctk.CTkButton(
            self,
            text="🔔",
            width=30,
            command=self.abrir_notificacoes
        )
        self.btn_notificacoes.pack(padx=5, pady=5)
        
    def abrir_notificacoes(self):
        popup = NotificacoesPopup(self, self.usuario_id)
        popup.focus()
