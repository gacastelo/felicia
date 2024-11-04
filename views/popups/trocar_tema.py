import customtkinter as ctk
from typing import Dict, List
import json
from pathlib import Path

class TrocarTemaPopup(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        
        # Configurações da janela
        self.title("Trocar Tema")
        self.geometry("300x200")
        self.grab_set()  # Torna a janela modal
        self.focus_force()  # Força o foco para esta janela
        self.lift()  # Traz a janela para frente
        
        # Centralizar na tela
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_width()) // 2
        y = (self.winfo_screenheight() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
        
        # Carregar configurações salvas
        self.config_path = Path("data/tema_config.json")
        self.config_path.parent.mkdir(exist_ok=True)
        self.carregar_configuracoes()
        
        self._criar_widgets()
        
        # Protocolo para quando a janela for fechada
        self.protocol("WM_DELETE_WINDOW", self._ao_fechar)
    
    def carregar_configuracoes(self):
        """Carrega as configurações salvas ou usa padrões"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "modo": "dark",
                "cor_primaria": "blue",
                "cor_secundaria": "gray"
            }
    
    def salvar_configuracoes(self):
        """Salva as configurações atuais"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def _criar_widgets(self):
        # Frame principal
        frame_principal = ctk.CTkFrame(self)
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo = ctk.CTkLabel(
            frame_principal,
            text="Configurações de Tema",
            font=("Roboto", 20, "bold")
        )
        titulo.pack(pady=10)
        
        # Frame para modo de aparência
        frame_modo = ctk.CTkFrame(frame_principal)
        frame_modo.pack(fill="x", pady=10)
        
        # Label para modo
        label_modo = ctk.CTkLabel(
            frame_modo,
            text="Modo de Aparência:",
            font=("Roboto", 14)
        )
        label_modo.pack(pady=5)
        
        # Segmented button para modo
        self.modo_var = ctk.StringVar(value=self.config["modo"])
        self.modo_selector = ctk.CTkSegmentedButton(
            frame_modo,
            values=["Light", "Dark", "System"],
            variable=self.modo_var,
            command=self._preview_tema
        )
        self.modo_selector.pack(pady=5)
        
        # Frame para cores
        frame_cores = ctk.CTkFrame(frame_principal)
        frame_cores.pack(fill="x", pady=10)
        
        # Label para cores
        label_cores = ctk.CTkLabel(
            frame_cores,
            text="Esquema de Cores:",
            font=("Roboto", 14)
        )
        label_cores.pack(pady=5)
        
        # Opções de cores
        cores_disponiveis: List[str] = [
            "blue", "green", "dark-blue", 
            "purple", "brown", "teal"
        ]
        self.cor_var = ctk.StringVar(value=self.config["cor_primaria"])
        
        for cor in cores_disponiveis:
            frame_cor = ctk.CTkFrame(frame_cores)
            frame_cor.pack(fill="x", pady=2)
            
            # Exemplo visual da cor
            exemplo_cor = ctk.CTkButton(
                frame_cor,
                text="",
                width=30,
                height=20,
                fg_color=cor,
                hover_color=cor
            )
            exemplo_cor.pack(side="left", padx=5)
            
            # Radio button para seleção
            radio_cor = ctk.CTkRadioButton(
                frame_cor,
                text=cor.title(),
                variable=self.cor_var,
                value=cor,
                command=self._preview_tema
            )
            radio_cor.pack(side="left", padx=5)
        
        # Frame para botões
        frame_botoes = ctk.CTkFrame(frame_principal)
        frame_botoes.pack(pady=20)
        
        # Botão aplicar
        btn_aplicar = ctk.CTkButton(
            frame_botoes,
            text="Aplicar",
            command=self._aplicar_tema
        )
        btn_aplicar.pack(side="left", padx=5)
        
        # Botão cancelar
        btn_cancelar = ctk.CTkButton(
            frame_botoes,
            text="Cancelar",
            command=self._restaurar_tema
        )
        btn_cancelar.pack(side="left", padx=5)
        
        # Salvar tema atual para possível restauração
        self.tema_anterior = {
            "modo": ctk.get_appearance_mode(),
            "cor": ctk.get_default_color_theme()
        }
    
    def _preview_tema(self, *args):
        """Aplica o tema selecionado em tempo real"""
        modo = self.modo_var.get().lower()
        cor = self.cor_var.get()
        
        ctk.set_appearance_mode(modo)
        ctk.set_default_color_theme(cor)
        
        # Atualiza configuração atual
        self.config["modo"] = modo
        self.config["cor_primaria"] = cor
    
    def _aplicar_tema(self):
        """Salva e aplica o tema selecionado"""
        self.salvar_configuracoes()
        
        # Atualiza o tema no aplicativo principal
        self.master.master.trocar_tema(self.config["modo"])
        
        self._mostrar_sucesso("Tema aplicado com sucesso!")
        self.destroy()
    
    def _restaurar_tema(self):
        """Restaura o tema anterior e fecha o popup"""
        ctk.set_appearance_mode(self.tema_anterior["modo"])
        ctk.set_default_color_theme(self.tema_anterior["cor"])
        self.destroy()
    
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