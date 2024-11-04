from views.popups.base_popup import BasePopup
import customtkinter as ctk

class BackupPopup(BasePopup):
    def __init__(self, master):
        super().__init__(master, "Backup", 400, 300)
        self._criar_widgets()
    
    def _criar_widgets(self):
        # Frame principal com fundo transparente
        frame_principal = ctk.CTkFrame(self, fg_color="transparent")
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo = ctk.CTkLabel(
            frame_principal,
            text="Backup e Restauração",
            font=("Roboto", 20, "bold")
        )
        titulo.pack(pady=(0, 20))
        
        # Frame para botões com fundo transparente
        frame_botoes = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_botoes.pack(fill="both", expand=True)
        
        # Botões
        btn_exportar = ctk.CTkButton(
            frame_botoes, 
            text="Exportar Backup", 
            command=self._exportar,
            width=200,
            height=40,
            fg_color="#8E7CC3",  # roxinho fofo
            hover_color="#7667a3"  # roxinho fofo mais escuro
        )
        btn_exportar.pack(pady=10)
        
        btn_importar = ctk.CTkButton(
            frame_botoes, 
            text="Importar Backup", 
            command=self._importar,
            width=200,
            height=40,
            fg_color="#8E7CC3",  # roxinho fofo
            hover_color="#7667a3"  # roxinho fofo mais escuro
        )
        btn_importar.pack(pady=10)
        
        btn_fechar = ctk.CTkButton(
            frame_botoes, 
            text="Fechar", 
            command=self.destroy,
            width=200,
            height=40,
            fg_color="#8E7CC3",  # roxinho fofo
            hover_color="#7667a3"  # roxinho fofo mais escuro
        )
        btn_fechar.pack(pady=10)
    
    def _exportar(self):
        sucesso, mensagem = self.master.master.backup_service.exportar_backup(
            self.master.master.auth_controller.usuario_atual.id
        )
        
        if sucesso:
            self.master._mostrar_sucesso(mensagem)
        else:
            self.master._mostrar_erro(mensagem)
    
    def _importar(self):
        sucesso, mensagem = self.master.master.backup_service.importar_backup(
            self.master.master.auth_controller.usuario_atual.id
        )
        
        if sucesso:
            self.master._mostrar_sucesso(mensagem)
            self.master._atualizar_lista()
        else:
            self.master._mostrar_erro(mensagem)