from views.popups.base_popup import BasePopup
import customtkinter as ctk
import string
import secrets
import pyperclip

class AdicionarSenhaPopup(BasePopup):
    def __init__(self, master):
        super().__init__(master, "Adicionar Senha")
        self._criar_widgets()
    
    def _criar_widgets(self):
        # Frame principal
        frame_principal = ctk.CTkFrame(self)
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        titulo = ctk.CTkLabel(
            frame_principal,
            text="Adicionar Nova Senha",
            font=("Roboto", 20, "bold")
        )
        titulo.pack(pady=10)
        
        # Campos de entrada
        self.site_entry = ctk.CTkEntry(
            frame_principal,
            placeholder_text="Nome do site",
            width=300
        )
        self.site_entry.pack(pady=10)
        
        self.username_entry = ctk.CTkEntry(
            frame_principal,
            placeholder_text="Nome de usuário (opcional)",
            width=300
        )
        self.username_entry.pack(pady=10)
        
        # Frame para senha
        frame_senha = ctk.CTkFrame(frame_principal)
        frame_senha.pack(fill="x", pady=10)
        
        self.senha_entry = ctk.CTkEntry(
            frame_senha,
            placeholder_text="Senha",
            show="•",
            width=240
        )
        self.senha_entry.pack(side="left", padx=5)
        
        # Botões de senha
        btn_mostrar = ctk.CTkButton(
            frame_senha,
            text="👁",
            width=30,
            command=self._toggle_mostrar_senha
        )
        btn_mostrar.pack(side="left", padx=2)
        
        btn_gerar = ctk.CTkButton(
            frame_senha,
            text="Gerar",
            width=60,
            command=self._gerar_senha
        )
        btn_gerar.pack(side="left", padx=2)
        
        # Opções de geração de senha
        frame_opcoes = ctk.CTkFrame(frame_principal)
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
        frame_checks = ctk.CTkFrame(frame_principal)
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
        
        # Botões de ação - Agora em um frame separado no final
        frame_botoes = ctk.CTkFrame(self)  # Note que agora é filho direto do self
        frame_botoes.pack(side="bottom", pady=20)
        
        btn_salvar = ctk.CTkButton(
            frame_botoes,
            text="Salvar",
            command=self._salvar,
            width=100
        )
        btn_salvar.pack(side="left", padx=5)
        
        btn_cancelar = ctk.CTkButton(
            frame_botoes,
            text="Cancelar",
            command=self.destroy,
            width=100
        )
        btn_cancelar.pack(side="left", padx=5)
        
        btn_copiar = ctk.CTkButton(
            frame_botoes,
            text="Copiar",
            command=self._copiar_senha,
            width=100
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