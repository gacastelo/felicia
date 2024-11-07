from views.popups.base_popup import BasePopup
import customtkinter as ctk

class TrocarTemaPopup(BasePopup):
    def __init__(self, master):
        super().__init__(master, "Configurações de Aparência", 600, 700)
        self._criar_widgets()
    
    def _criar_widgets(self):
        # Frame principal
        frame_principal = ctk.CTkFrame(self, fg_color="transparent")
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Seção de Tema
        label_tema = ctk.CTkLabel(
            frame_principal, 
            text="Tema:",
            font=("Roboto", int(16 * self.escala), "bold")
        )
        label_tema.pack(pady=(20, 10))
        
        # Frame para botões de tema
        frame_temas = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_temas.pack(pady=10, fill="x")
        
        # Grid configuration para os botões de tema
        frame_temas.grid_columnconfigure(0, weight=1)
        frame_temas.grid_columnconfigure(1, weight=1)
        
        # Botões de tema em grid
        temas = [("Claro", "light"), ("Escuro", "dark")]
        for i, (nome, valor) in enumerate(temas):
            btn = ctk.CTkButton(
                frame_temas,
                text=nome,
                command=lambda t=valor: self._trocar_tema(t),
                width=int(120 * self.escala),
                height=int(35 * self.escala),
                font=("Roboto", int(14 * self.escala)),
                fg_color="#8E7CC3",
                hover_color="#7667a3"
            )
            btn.grid(row=0, column=i, padx=10, pady=5, sticky="ew")
        
        # Seção de Tamanho da Fonte
        label_fonte = ctk.CTkLabel(
            frame_principal, 
            text="Tamanho da Fonte:",
            font=("Roboto", int(16 * self.escala), "bold")
        )
        label_fonte.pack(pady=(30, 10))
        
        # Frame para grid de botões de fonte
        frame_fontes = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_fontes.pack(pady=10, fill="x")
        
        # Grid configuration para os botões de fonte
        frame_fontes.grid_columnconfigure(0, weight=1)
        frame_fontes.grid_columnconfigure(1, weight=1)
        
        # Configuração dos tamanhos em grid
        tamanhos = [
            ("Pequena", 11),
            ("Média", 13),
            ("Grande", 15),
            ("Maior", 17)
        ]
        
        # Criar grid para os botões
        for i, (nome, tamanho) in enumerate(tamanhos):
            row = i // 2
            col = i % 2
            
            btn = ctk.CTkButton(
                frame_fontes,
                text=nome,
                command=lambda t=tamanho: self._trocar_tamanho_fonte(t),
                width=int(120 * self.escala),
                height=int(35 * self.escala),
                font=("Roboto", int(14 * self.escala)),
                fg_color="#8E7CC3",
                hover_color="#7667a3"
            )
            btn.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
        
        # Botão fechar
        btn_fechar = ctk.CTkButton(
            frame_principal, 
            text="Fechar", 
            command=self._fechar,
            width=int(120 * self.escala),
            height=int(35 * self.escala),
            font=("Roboto", int(14 * self.escala)),
            fg_color="#8E7CC3",
            hover_color="#7667a3"
        )
        btn_fechar.pack(pady=30)
    
    def _get_bg_color(self):
        """Retorna a cor de fundo baseada no tema atual"""
        return "#333333" if ctk.get_appearance_mode() == "Dark" else "#EEEEEE"
    
    def _trocar_tema(self, tema):
        try:
            self.master.master.trocar_tema(tema)
            self.master._mostrar_sucesso(f"Tema alterado para {tema}")
            self._fechar()
        except Exception as e:
            self.master._mostrar_erro(f"Erro ao trocar tema: {str(e)}")
    
    def _trocar_tamanho_fonte(self, tamanho):
        try:
            self.master.master.trocar_tamanho_fonte(tamanho)
            self.master._mostrar_sucesso(f"Tamanho da fonte alterado")
            self._fechar()
        except Exception as e:
            self.master._mostrar_erro(f"Erro ao trocar tamanho da fonte: {str(e)}")
    
    def _fechar(self):
        """Método seguro para fechar o popup"""
        try:
            self.destroy()
        except Exception as e:
            print(f"Erro ao fechar popup: {str(e)}")