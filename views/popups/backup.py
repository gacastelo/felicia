from views.popups.base_popup import BasePopup
import customtkinter as ctk

class BackupPopup(BasePopup):
    def __init__(self, master):
        super().__init__(master, "Backup", 400, 300)
        self._criar_widgets()
    
    def _criar_widgets(self):
        # Frame principal
        frame = ctk.CTkFrame(self)
        frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Botões
        btn_exportar = ctk.CTkButton(frame, text="Exportar Backup", command=self._exportar)
        btn_exportar.pack(pady=10)
        
        btn_importar = ctk.CTkButton(frame, text="Importar Backup", command=self._importar)
        btn_importar.pack(pady=10)
        
        btn_fechar = ctk.CTkButton(frame, text="Fechar", command=self.destroy)
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