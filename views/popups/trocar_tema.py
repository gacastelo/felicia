from views.popups.base_popup import BasePopup
import customtkinter as ctk

class TrocarTemaPopup(BasePopup):
    def __init__(self, master):
        super().__init__(master, "Configurações de Aparência", 500, 600)
        self._criar_widgets()
    
    def _criar_widgets(self):
        # Frame principal
        frame = ctk.CTkFrame(self)
        frame.pack(padx=int(20 * self.escala), 
                  pady=int(20 * self.escala), 
                  fill="both", 
                  expand=True)
        
        # Seção de Tema
        label_tema = ctk.CTkLabel(
            frame, 
            text="Tema:",
            font=("Roboto", int(16 * self.escala), "bold")
        )
        label_tema.pack(pady=(int(20 * self.escala), int(10 * self.escala)))
        
        # Frame para botões de tema
        frame_temas = ctk.CTkFrame(frame, fg_color="transparent")
        frame_temas.pack(pady=int(10 * self.escala))
        
        # Botões de tema
        temas = [("Claro", "light"), ("Escuro", "dark")]
        for nome, valor in temas:
            btn = ctk.CTkButton(
                frame_temas,
                text=nome,
                command=lambda t=valor: self._trocar_tema(t),
                width=int(150 * self.escala),
                height=int(35 * self.escala),
                font=("Roboto", int(14 * self.escala)),
                fg_color="#8E7CC3",
                hover_color="#7667a3"
            )
            btn.pack(side="left", padx=int(10 * self.escala))
        
        # Seção de Tamanho da Fonte
        label_fonte = ctk.CTkLabel(
            frame, 
            text="Tamanho da Fonte:",
            font=("Roboto", int(16 * self.escala), "bold")
        )
        label_fonte.pack(pady=(int(30 * self.escala), int(10 * self.escala)))
        
        # Frame para grid de botões de fonte
        frame_fontes = ctk.CTkFrame(frame, fg_color="transparent")
        frame_fontes.pack(pady=int(10 * self.escala))
        
        # Configuração dos tamanhos em grid 2x2
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
                width=int(150 * self.escala),
                height=int(35 * self.escala),
                font=("Roboto", int(14 * self.escala)),
                fg_color="#8E7CC3",
                hover_color="#7667a3"
            )
            btn.grid(row=row, column=col, padx=int(5 * self.escala), 
                    pady=int(5 * self.escala))
        
        # Configurar o grid
        frame_fontes.grid_columnconfigure(0, weight=1)
        frame_fontes.grid_columnconfigure(1, weight=1)
        
        # Botão fechar
        btn_fechar = ctk.CTkButton(
            frame, 
            text="Fechar", 
            command=self._fechar,
            width=int(150 * self.escala),
            height=int(35 * self.escala),
            font=("Roboto", int(14 * self.escala)),
            fg_color="#8E7CC3",
            hover_color="#7667a3"
        )
        btn_fechar.pack(pady=int(30 * self.escala))
    
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
            # Desabilita todos os botões antes de fechar
            for widget in self.winfo_children():
                if isinstance(widget, ctk.CTkButton):
                    widget.configure(state="disabled")
            
            # Remove o foco do popup
            self.grab_release()
            
            # Destrói o popup
            self.destroy()
        except Exception as e:
            print(f"Erro ao fechar popup: {e}")