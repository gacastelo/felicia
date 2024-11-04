import customtkinter as ctk
from .base_popup import BasePopup

class MensagemPopup(BasePopup):
    def __init__(self, master, titulo, mensagem):
        # Tamanho base ajustado pela escala
        super().__init__(master, titulo, largura=300, altura=150)
        
        # Frame principal
        self.frame_conteudo = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_conteudo.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Label com a mensagem - ajusta wraplength pela escala
        label = ctk.CTkLabel(
            self.frame_conteudo,
            text=mensagem,
            font=("Roboto", int(12 * self.escala)),
            wraplength=int(250 * self.escala)
        )
        label.pack(pady=20)
        
        # Botão de OK - ajusta width pela escala
        btn_ok = ctk.CTkButton(
            self.frame_conteudo,
            text="OK",
            command=self.destroy,
            width=int(100 * self.escala),
            height=int(32 * self.escala),
            font=("Roboto", int(12 * self.escala)),
            fg_color="#8E7CC3",
            hover_color="#7667a3"
        )
        btn_ok.pack(pady=10)