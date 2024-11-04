from views.popups.base_popup import BasePopup
import customtkinter as ctk

class MensagemPopup(BasePopup):
    def __init__(self, master, titulo, mensagem, largura=300, altura=150):
        super().__init__(master, titulo, largura, altura)
        
        # Label com a mensagem
        label = ctk.CTkLabel(self, text=mensagem)
        label.pack(pady=20)
        
        # Botão OK
        btn = ctk.CTkButton(self, text="OK", command=self.destroy)
        btn.pack(pady=10) 