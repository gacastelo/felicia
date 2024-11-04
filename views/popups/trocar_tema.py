from views.popups.base_popup import BasePopup
import customtkinter as ctk

class TrocarTemaPopup(BasePopup):
    def __init__(self, master):
        super().__init__(master, "Trocar Tema", 400, 300)
        self._criar_widgets()
    
    def _criar_widgets(self):
        # Frame principal
        frame = ctk.CTkFrame(self)
        frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Label
        label = ctk.CTkLabel(frame, text="Selecione o tema:")
        label.pack(pady=10)
        
        # Botões de tema
        temas = [("Claro", "light"), ("Escuro", "dark"), ("Sistema", "system")]
        
        for nome, valor in temas:
            btn = ctk.CTkButton(
                frame,
                text=nome,
                command=lambda t=valor: self._trocar_tema(t)
            )
            btn.pack(pady=5)
        
        # Botão fechar
        btn_fechar = ctk.CTkButton(frame, text="Fechar", command=self.destroy)
        btn_fechar.pack(pady=20)
    
    def _trocar_tema(self, tema):
        try:
            self.master.master.trocar_tema(tema)
            self.master._mostrar_sucesso(f"Tema alterado para {tema}")
            self.destroy()
        except Exception as e:
            self.master._mostrar_erro(f"Erro ao trocar tema: {str(e)}")