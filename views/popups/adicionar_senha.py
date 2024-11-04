from views.popups.base_senha_popup import BaseSenhaPopup
import customtkinter as ctk
import string
import secrets
import pyperclip

class AdicionarSenhaPopup(BaseSenhaPopup):
    def __init__(self, master):
        super().__init__(master, "Adicionar Senha", largura=600, altura=500)
        self._criar_widgets()
    
    def _criar_widgets(self):
        # Frame principal
        frame_principal = ctk.CTkFrame(self, fg_color="transparent")
        frame_principal.pack(fill="both", expand=True, 
                           padx=int(20 * self.escala), 
                           pady=int(20 * self.escala))
        
        # Título
        titulo = ctk.CTkLabel(
            frame_principal,
            text="Adicionar Nova Senha",
            font=("Roboto", int(20 * self.escala), "bold")
        )
        titulo.pack(pady=int(10 * self.escala))
        
        # Campos de entrada
        self.site_entry = ctk.CTkEntry(
            frame_principal,
            placeholder_text="Nome do site",
            width=int(300 * self.escala),
            height=int(35 * self.escala),
            font=("Roboto", int(12 * self.escala))
        )
        self.site_entry.pack(pady=int(10 * self.escala))
        
        self.username_entry = ctk.CTkEntry(
            frame_principal,
            placeholder_text="Nome de usuário (opcional)",
            width=int(300 * self.escala),
            height=int(35 * self.escala),
            font=("Roboto", int(12 * self.escala))
        )
        self.username_entry.pack(pady=int(10 * self.escala))
        
        # Frame para senha (agora centralizado)
        frame_senha = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_senha.pack(pady=int(10 * self.escala))
        
        # Container para manter os elementos alinhados
        senha_container = ctk.CTkFrame(frame_senha, fg_color="transparent")
        senha_container.pack(expand=True)
        
        self.senha_entry = ctk.CTkEntry(
            senha_container,
            placeholder_text="Senha",
            show="•",
            width=int(240 * self.escala),
            height=int(35 * self.escala),
            font=("Roboto", int(12 * self.escala))
        )
        self.senha_entry.pack(side="left")
        
        btn_mostrar = ctk.CTkButton(
            senha_container,
            text="👁",
            width=int(30 * self.escala),
            height=int(35 * self.escala),
            command=self._toggle_mostrar_senha,
            fg_color="#8E7CC3",
            hover_color="#7667a3",
            font=("Roboto", int(12 * self.escala))
        )
        btn_mostrar.pack(side="left", padx=int(2 * self.escala))
        
        btn_gerar = ctk.CTkButton(
            senha_container,
            text="Gerar",
            width=int(60 * self.escala),
            height=int(35 * self.escala),
            command=self._gerar_senha,
            fg_color="#8E7CC3",
            hover_color="#7667a3",
            font=("Roboto", int(12 * self.escala))
        )
        btn_gerar.pack(side="left", padx=int(2 * self.escala))
        
        # Opções de geração de senha
        frame_opcoes = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_opcoes.pack(fill="x", pady=int(10 * self.escala))
        
        # Tamanho da senha
        label_tamanho = ctk.CTkLabel(frame_opcoes, text="Tamanho:")
        label_tamanho.pack(side="left", padx=int(5 * self.escala))
        
        self.tamanho_var = ctk.IntVar(value=16)
        self.tamanho_entry = ctk.CTkEntry(
            frame_opcoes,
            width=int(50 * self.escala),
            textvariable=self.tamanho_var,
            font=("Roboto", int(12 * self.escala))
        )
        self.tamanho_entry.pack(side="left", padx=int(5 * self.escala))
        
        # Checkboxes
        frame_checks = ctk.CTkFrame(frame_principal, fg_color="transparent")
        frame_checks.pack(fill="x", pady=int(10 * self.escala))
        
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
            check.pack(side="left", padx=int(5 * self.escala))
        
        # Botões de ação
        frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        frame_botoes.pack(side="bottom", pady=int(20 * self.escala))
        
        btn_salvar = ctk.CTkButton(
            frame_botoes,
            text="Salvar",
            command=self._salvar,
            width=int(100 * self.escala),
            fg_color="#8E7CC3",  # roxinho fofo
            hover_color="#7667a3",  # roxinho fofo mais escuro
            font=("Roboto", int(12 * self.escala))
        )
        btn_salvar.pack(side="left", padx=int(5 * self.escala))
        
        btn_cancelar = ctk.CTkButton(
            frame_botoes,
            text="Cancelar",
            command=self.destroy,
            width=int(100 * self.escala),
            fg_color="#8E7CC3",  # roxinho fofo
            hover_color="#7667a3",  # roxinho fofo mais escuro
            font=("Roboto", int(12 * self.escala))
        )
        btn_cancelar.pack(side="left", padx=int(5 * self.escala))
        
        btn_copiar = ctk.CTkButton(
            frame_botoes,
            text="Copiar",
            command=self._copiar_senha,
            width=int(100 * self.escala),
            fg_color="#8E7CC3",  # roxinho fofo
            hover_color="#7667a3",  # roxinho fofo mais escuro
            font=("Roboto", int(12 * self.escala))
        )
        btn_copiar.pack(side="left", padx=int(5 * self.escala))
    
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
            self.master._mostrar_sucesso(mensagem)
            self.master._atualizar_lista()
            self.destroy()
        else:
            self.master._mostrar_erro(mensagem)