import customtkinter as ctk
from utils.backup import BackupService
from pathlib import Path
from tkinter import filedialog
from datetime import datetime

class BackupPopup(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.backup_service = BackupService()
        
        # Configurações da janela
        self.title("Backup")
        self.geometry("400x300")
        self.grab_set()  # Torna a janela modal
        self.focus_force()  # Força o foco para esta janela
        self.lift()  # Traz a janela para frente
        
        # Centralizar na tela
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_width()) // 2
        y = (self.winfo_screenheight() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
        
        self._criar_widgets()
        self._atualizar_lista()
        
        # Protocolo para quando a janela for fechada
        self.protocol("WM_DELETE_WINDOW", self._ao_fechar)
    
    def _criar_widgets(self):
        # Frame principal
        frame_principal = ctk.CTkFrame(self)
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo = ctk.CTkLabel(
            frame_principal,
            text="Gerenciamento de Backups",
            font=("Roboto", 20, "bold")
        )
        titulo.pack(pady=10)
        
        # Frame para botões
        frame_botoes = ctk.CTkFrame(frame_principal)
        frame_botoes.pack(fill="x", pady=10)
        
        # Botões
        btn_criar = ctk.CTkButton(
            frame_botoes,
            text="Criar Backup",
            command=self._criar_backup
        )
        btn_criar.pack(side="left", padx=5)
        
        btn_restaurar = ctk.CTkButton(
            frame_botoes,
            text="Restaurar Backup",
            command=self._restaurar_backup
        )
        btn_restaurar.pack(side="left", padx=5)
        
        # Lista de backups
        self.frame_lista = ctk.CTkScrollableFrame(frame_principal)
        self.frame_lista.pack(fill="both", expand=True, pady=10)
    
    def _atualizar_lista(self):
        # Limpa a lista atual
        for widget in self.frame_lista.winfo_children():
            widget.destroy()
        
        # Lista os backups
        backups = self.backup_service.listar_backups()
        
        for backup in backups:
            frame_item = ctk.CTkFrame(self.frame_lista)
            frame_item.pack(fill="x", pady=2)
            
            # Nome do backup
            label_nome = ctk.CTkLabel(
                frame_item,
                text=backup.name,
                anchor="w"
            )
            label_nome.pack(side="left", padx=5)
            
            # Data do backup
            data = backup.stat().st_mtime
            data_str = datetime.fromtimestamp(data).strftime("%d/%m/%Y %H:%M")
            label_data = ctk.CTkLabel(
                frame_item,
                text=data_str,
                anchor="w"
            )
            label_data.pack(side="left", padx=5)
    
    def _criar_backup(self):
        sucesso, mensagem = self.backup_service.criar_backup(
            self.master.master.auth_controller.usuario_atual.id
        )
        
        if sucesso:
            self._mostrar_sucesso(mensagem)
            self._atualizar_lista()
        else:
            self._mostrar_erro(mensagem)
    
    def _restaurar_backup(self):
        arquivo = filedialog.askopenfilename(
            title="Selecionar backup",
            filetypes=[("Arquivo ZIP", "*.zip")],
            initialdir=self.backup_service.backup_dir
        )
        
        if arquivo:
            sucesso, mensagem = self.backup_service.restaurar_backup(Path(arquivo))
            
            if sucesso:
                self._mostrar_sucesso(mensagem)
                self.master.master.auth_controller.logout()
                self.master.destroy()
            else:
                self._mostrar_erro(mensagem)
    
    def _mostrar_erro(self, mensagem):
        erro = ctk.CTkToplevel(self)
        erro.title("Erro")
        erro.geometry("300x150")
        
        erro.update_idletasks()
        x = (erro.winfo_screenwidth() - erro.winfo_width()) // 2
        y = (erro.winfo_screenheight() - erro.winfo_height()) // 2
        erro.geometry(f"+{x}+{y}")
        
        label = ctk.CTkLabel(erro, text=mensagem)
        label.pack(pady=20)
        
        btn = ctk.CTkButton(erro, text="OK", command=erro.destroy)
        btn.pack(pady=10)
    
    def _mostrar_sucesso(self, mensagem):
        sucesso = ctk.CTkToplevel(self)
        sucesso.title("Sucesso")
        sucesso.geometry("300x150")
        
        sucesso.update_idletasks()
        x = (sucesso.winfo_screenwidth() - sucesso.winfo_width()) // 2
        y = (sucesso.winfo_screenheight() - sucesso.winfo_height()) // 2
        sucesso.geometry(f"+{x}+{y}")
        
        label = ctk.CTkLabel(sucesso, text=mensagem)
        label.pack(pady=20)
        
        btn = ctk.CTkButton(sucesso, text="OK", command=sucesso.destroy)
        btn.pack(pady=10)
    
    def _ao_fechar(self):
        """Método chamado quando a janela é fechada"""
        self.grab_release()  # Libera o modo modal
        self.destroy()  # Destrói a janela