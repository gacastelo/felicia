from views.popups.base_senha_popup import BaseSenhaPopup
import customtkinter as ctk
import string
import secrets
import pyperclip

class AdicionarSenhaPopup(BaseSenhaPopup):
    def __init__(self, master):
        super().__init__(master, "Adicionar Senha", largura=600, altura=500)
        # Configurações de aparência
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self._criar_widgets()
    
    def _criar_widgets(self):
        # Frame principal
        frame_principal = ctk.CTkFrame(self, fg_color="transparent")
        frame_principal.pack(fill="both", expand=True, padx=int(20 * self.escala))
        
        # Título
        titulo = ctk.CTkLabel(
            frame_principal,
            text="Adicionar Nova Senha",
            font=("Roboto", int(20 * self.escala), "bold")
        )
        titulo.pack(pady=(int(10 * self.escala), int(20 * self.escala)))
        
        # Campos de entrada
        self.site_entry = ctk.CTkEntry(
            frame_principal,
            placeholder_text="Nome do site",
            width=int(300 * self.escala),
            height=int(35 * self.escala)
        )
        self.site_entry.pack(pady=(0, int(10 * self.escala)))
        
        self.username_entry = ctk.CTkEntry(
            frame_principal,
            placeholder_text="Nome de usuário (opcional)",
            width=int(300 * self.escala),
            height=int(35 * self.escala)
        )
        self.username_entry.pack(pady=(0, int(10 * self.escala)))
        
        # Frame da senha sem padding extra
        frame_senha = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_senha.pack(fill="x", pady=(0, int(5 * self.escala)))  # Reduzido padding inferior
        
        container_senha = ctk.CTkFrame(frame_senha, fg_color="transparent", width=int(300 * self.escala))
        container_senha.pack(expand=False)
        container_senha.pack_propagate(False)
        
        frame_elementos_senha = ctk.CTkFrame(container_senha, fg_color="transparent")
        frame_elementos_senha.pack(fill="x")
        
        self.senha_entry = ctk.CTkEntry(
            frame_elementos_senha,
            placeholder_text="Senha",
            show="•",
            height=int(35 * self.escala),
            font=("Roboto", int(12 * self.escala))
        )
        self.senha_entry.pack(side="left", expand=True, fill="x", padx=(0, int(5 * self.escala)))
        
        btn_mostrar = ctk.CTkButton(
            frame_elementos_senha,
            text="👁",
            width=int(35 * self.escala),
            height=int(35 * self.escala),
            command=self._toggle_mostrar_senha,
            fg_color="#8E7CC3",
            hover_color="#7667a3"
        )
        btn_mostrar.pack(side="left", padx=int(2 * self.escala))
        
        btn_gerar = ctk.CTkButton(
            frame_elementos_senha,
            text="Gerar",
            width=int(50 * self.escala),
            height=int(35 * self.escala),
            command=self._gerar_senha,
            fg_color="#8E7CC3",
            hover_color="#7667a3"
        )
        btn_gerar.pack(side="left", padx=int(2 * self.escala))
        
        # Frame das opções - removido padding do topo
        frame_opcoes = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_opcoes.pack(fill="x", pady=(0, int(5 * self.escala)))  # Apenas padding inferior
        
        # Container para tamanho - ajustado padding
        frame_tamanho = ctk.CTkFrame(frame_opcoes, fg_color="transparent")
        frame_tamanho.pack(anchor="w", padx=int(10 * self.escala))  # Mudado para anchor="w"
        
        ctk.CTkLabel(
            frame_tamanho,
            text="Tamanho:",
            font=("Roboto", int(12 * self.escala))
        ).pack(side="left")
        
        self.tamanho_var = ctk.StringVar(value="16")
        self.tamanho_entry = ctk.CTkEntry(
            frame_tamanho,
            textvariable=self.tamanho_var,
            width=int(50 * self.escala),
            height=int(25 * self.escala),
            font=("Roboto", int(12 * self.escala))
        )
        self.tamanho_entry.pack(side="left", padx=int(5 * self.escala))
        
        # Frame das checkboxes - ajustado padding
        frame_checks = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_checks.pack(fill="x", pady=(0, int(5 * self.escala)))
        
        # Container para centralizar as checkboxes
        container_checks = ctk.CTkFrame(frame_checks, fg_color="transparent")
        container_checks.pack(expand=True)
        
        self.maiusculas_var = ctk.BooleanVar(value=True)
        self.minusculas_var = ctk.BooleanVar(value=True)
        self.numeros_var = ctk.BooleanVar(value=True)
        self.especiais_var = ctk.BooleanVar(value=True)
        
        opcoes = [
            ("Maiúsculas", self.maiusculas_var),
            ("Minúsculas", self.minusculas_var),
            ("Números", self.numeros_var),
            ("Especiais", self.especiais_var)
        ]
        
        for texto, var in opcoes:
            check = ctk.CTkCheckBox(container_checks, text=texto, variable=var)
            check.pack(side="left", padx=5)
        
        # Estilo da animação de hover
        def on_enter(e):
            e.widget.configure(fg_color="#9982D0")  # Cor mais clara

        def on_leave(e):
            e.widget.configure(fg_color="#8E7CC3")  # Cor original
        
        # Frame dos botões com novo layout
        frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        frame_botoes.pack(side="bottom", pady=20)
        
        # Botões com novos estilos e animações
        btn_salvar = ctk.CTkButton(
            frame_botoes,
            text="Salvar",
            command=self._salvar,
            width=int(140 * self.escala),
            height=int(45 * self.escala),
            fg_color="#8E7CC3",
            hover_color="#7667a3",
            font=("Roboto", int(15 * self.escala))
        )
        btn_salvar.pack(side="left", padx=int(10 * self.escala))
        btn_salvar.bind("<Enter>", on_enter)
        btn_salvar.bind("<Leave>", on_leave)
        
        btn_cancelar = ctk.CTkButton(
            frame_botoes,
            text="Cancelar",
            command=self.destroy,
            width=int(140 * self.escala),
            height=int(45 * self.escala),
            fg_color="#8E7CC3",
            hover_color="#7667a3",
            font=("Roboto", int(15 * self.escala))
        )
        btn_cancelar.pack(side="left", padx=int(10 * self.escala))
        btn_cancelar.bind("<Enter>", on_enter)
        btn_cancelar.bind("<Leave>", on_leave)
        
        btn_copiar = ctk.CTkButton(
            frame_botoes,
            text="Copiar",
            command=self._copiar_senha,
            width=int(140 * self.escala),
            height=int(45 * self.escala),
            fg_color="#8E7CC3",
            hover_color="#7667a3",
            font=("Roboto", int(15 * self.escala))
        )
        btn_copiar.pack(side="left", padx=int(10 * self.escala))
        btn_copiar.bind("<Enter>", on_enter)
        btn_copiar.bind("<Leave>", on_leave)
    
    def _toggle_mostrar_senha(self):
        if self.senha_entry.cget("show") == "":
            self.senha_entry.configure(show="•")
        else:
            self.senha_entry.configure(show="")
    
    def _gerar_senha(self):
        try:
            tamanho = int(self.tamanho_var.get() or "16")  # Valor padrão se vazio
            if tamanho < 4:
                self.master._mostrar_erro("O tamanho mínimo é 4!")
                return
            if tamanho > 1024:
                self.master._mostrar_erro("O tamanho máximo é 1024!")
                return
        except ValueError:
            self.master._mostrar_erro("Tamanho inválido!")
            return
        
        caracteres = ""
        if self.maiusculas_var.get():
            caracteres += string.ascii_uppercase
        if self.minusculas_var.get():
            caracteres += string.ascii_lowercase
        if self.numeros_var.get():
            caracteres += string.digits
        if self.especiais_var.get():
            caracteres += string.punctuation
        
        if not caracteres:
            self.master._mostrar_erro("Selecione pelo menos uma opção!")
            return
        
        senha = ''.join(secrets.choice(caracteres) for _ in range(tamanho))
        self.senha_entry.delete(0, "end")
        self.senha_entry.insert(0, senha)
    
    def _copiar_senha(self):
        senha = self.senha_entry.get()
        if senha:
            pyperclip.copy(senha)
            self.senha_entry.configure(border_color="#50C878")  # Feedback visual verde
            self.master._mostrar_sucesso("Senha copiada para a área de transferência!")
            # Reset da cor da borda após 1 segundo
            self.after(1000, lambda: self.senha_entry.configure(border_color=""))
        else:
            self.master._mostrar_erro("Nenhuma senha para copiar!")
            self.senha_entry.configure(border_color="#FF6B6B")  # Feedback visual vermelho
            self.after(1000, lambda: self.senha_entry.configure(border_color=""))
    
    def _salvar(self):
        site = self.site_entry.get().strip()
        username = self.username_entry.get().strip()
        senha = self.senha_entry.get()
        
        # Validação básica
        if not site:
            self.master._mostrar_erro("O site é obrigatório!")
            return
            
        if not senha:
            self.master._mostrar_erro("A senha é obrigatória!")
            return
        
        # Chama o controller para adicionar a senha
        sucesso, mensagem = self.master.senha_controller.adicionar_senha(
            site=site,
            senha=senha,
            username=username
        )
        
        if sucesso:
            self.site_entry.configure(border_color="#50C878")  # Feedback visual verde
            self.master._mostrar_sucesso(mensagem)
            self.after(500, self.destroy)  # Fecha a janela após meio segundo
        else:
            self.site_entry.configure(border_color="#FF6B6B")  # Feedback visual vermelho
            self.master._mostrar_erro(mensagem)