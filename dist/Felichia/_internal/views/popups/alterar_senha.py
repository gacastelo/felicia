from views.popups.base_senha_popup import BaseSenhaPopup
import customtkinter as ctk
import string
import secrets
import pyperclip

class AlterarSenhaPopup(BaseSenhaPopup):
    def __init__(self, master, senha):
        super().__init__(master, "Alterar Senha", largura=600, altura=500)
        self.senha = senha
        self._criar_widgets()
        self._preencher_dados_atuais()
    
    def _criar_widgets(self):
        # Frame principal
        frame_principal = ctk.CTkFrame(self, fg_color="transparent")
        frame_principal.pack(fill="both", expand=True, 
                           padx=int(20 * self.escala), 
                           pady=int(20 * self.escala))
        
        # Título
        titulo = ctk.CTkLabel(
            frame_principal,
            text="Alterar Senha",
            font=("Roboto", 20, "bold")
        )
        titulo.pack(pady=10)
        
        # Campo para site
        self.site_entry = ctk.CTkEntry(
            frame_principal,
            placeholder_text="Nome do site",
            width=300
        )
        self.site_entry.pack(pady=10)
        
        # Campo para usuário
        self.username_entry = ctk.CTkEntry(
            frame_principal,
            placeholder_text="Nome de usuário (opcional)",
            width=300
        )
        self.username_entry.pack(pady=10)
        
        # Frame para senha
        frame_senha = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_senha.pack(fill="x", pady=10)
        
        # Campo para senha
        self.senha_entry = ctk.CTkEntry(
            frame_senha,
            placeholder_text="Nova senha",
            show="•",
            width=240
        )
        self.senha_entry.pack(side="left", padx=5)
        
        # Botões de senha
        btn_mostrar = ctk.CTkButton(
            frame_senha,
            text="👁",
            width=30,
            command=self._toggle_mostrar_senha,
            fg_color="#8E7CC3",  # roxinho fofo
            hover_color="#7667a3"  # roxinho fofo mais escuro
        )
        btn_mostrar.pack(side="left", padx=2)
        
        btn_gerar = ctk.CTkButton(
            frame_senha,
            text="Gerar",
            width=60,
            command=self._gerar_senha,
            fg_color="#8E7CC3",  # roxinho fofo
            hover_color="#7667a3"  # roxinho fofo mais escuro
        )
        btn_gerar.pack(side="left", padx=2)
        
        # Opções de geração de senha
        frame_opcoes = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_opcoes.pack(fill="x", pady=10)
        
        # Tamanho da senha
        label_tamanho = ctk.CTkLabel(frame_opcoes, text="Tamanho:")
        label_tamanho.pack(side="left", padx=5)
        
        self.tamanho_var = ctk.IntVar(value=16)
        self.tamanho_entry = ctk.CTkEntry(
            frame_opcoes,
            width=50,
            textvariable=self.tamanho_var
        )
        self.tamanho_entry.pack(side="left", padx=5)
        
        # Checkboxes
        frame_checks = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_checks.pack(fill="x", pady=10)
        
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
            check = ctk.CTkCheckBox(frame_checks, text=texto, variable=var)
            check.pack(side="left", padx=5)
        
        # Botões de ação
        frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        frame_botoes.pack(side="bottom", pady=20)
        
        btn_salvar = ctk.CTkButton(
            frame_botoes,
            text="Salvar",
            command=self._salvar,
            width=100,
            fg_color="#8E7CC3",  # roxinho fofo
            hover_color="#7667a3"  # roxinho fofo mais escuro
        )
        btn_salvar.pack(side="left", padx=5)
        
        btn_cancelar = ctk.CTkButton(
            frame_botoes,
            text="Cancelar",
            command=self.destroy,
            width=100,
            fg_color="#8E7CC3",  # roxinho fofo
            hover_color="#7667a3"  # roxinho fofo mais escuro
        )
        btn_cancelar.pack(side="left", padx=5)
        
        btn_copiar = ctk.CTkButton(
            frame_botoes,
            text="Copiar",
            command=self._copiar_senha,
            width=100,
            fg_color="#8E7CC3",  # roxinho fofo
            hover_color="#7667a3"  # roxinho fofo mais escuro
        )
        btn_copiar.pack(side="left", padx=5)
    
    def _toggle_mostrar_senha(self):
        if self.senha_entry.cget("show") == "":
            self.senha_entry.configure(show="•")
        else:
            self.senha_entry.configure(show="")
    
    def _gerar_senha(self):
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
        
        try:
            tamanho = self.tamanho_var.get()
            if tamanho < 4:
                self.master._mostrar_erro("O tamanho mínimo é 4!")
                return
        except:
            self.master._mostrar_erro("Tamanho inválido!")
            return
        
        senha = ''.join(secrets.choice(caracteres) for _ in range(tamanho))
        self.senha_entry.delete(0, "end")
        self.senha_entry.insert(0, senha)
    
    def _copiar_senha(self):
        senha = self.senha_entry.get()
        if senha:
            pyperclip.copy(senha)
            self.master._mostrar_sucesso("Senha copiada para a área de transferência!")
        else:
            self.master._mostrar_erro("Nenhuma senha para copiar!")
    
    def _preencher_dados_atuais(self):
        self.site_entry.insert(0, self.senha.site)
        if self.senha.username:
            self.username_entry.insert(0, self.senha.username)
    
    def _salvar(self):
        # Obtém os valores dos campos
        site = self.site_entry.get().strip()
        username = self.username_entry.get().strip()
        nova_senha = self.senha_entry.get()
        
        # Se campo estiver vazio, mantém valor original
        if not site:
            site = self.senha.site
        if not username:
            username = self.senha.username
        if not nova_senha:
            nova_senha = self.senha.senha
        
        # Verifica se houve alguma alteração
        if (site == self.senha.site and 
            username == self.senha.username and 
            nova_senha == self.senha.senha):
            self.master._mostrar_erro("Nenhuma alteração foi feita!")
            return
        
        # Validação básica
        if not site:
            self.master._mostrar_erro("O site é obrigatório!")
            return
        
        # Chama o controller para alterar a senha
        sucesso, mensagem = self.master.senha_controller.alterar_senha(
            id=self.senha.id,
            site=site,
            senha=nova_senha,
            username=username
        )
        
        if sucesso:
            self.master._mostrar_sucesso(mensagem)
            self.master._atualizar_lista()
            self.destroy()
        else:
            self.master._mostrar_erro(mensagem)