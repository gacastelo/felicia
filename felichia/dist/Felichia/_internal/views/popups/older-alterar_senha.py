import customtkinter as ctk
import string
import secrets
import pyperclip

class AlterarSenhaPopup(ctk.CTkToplevel):
    def __init__(self, master, senha_atual):
        super().__init__(master)
        self.master = master
        self.senha_atual = senha_atual
        
        # Configurações da janela
        self.title("Alterar Senha")
        self.geometry("400x500")
        self.grab_set()  # Torna a janela modal
        self.focus_force()  # Força o foco para esta janela
        self.lift()  # Traz a janela para frente
        
        # Centralizar na tela
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_width()) // 2
        y = (self.winfo_screenheight() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
        
        self._criar_widgets()
        self._preencher_dados_atuais()
        
        # Protocolo para quando a janela for fechada
        self.protocol("WM_DELETE_WINDOW", self._ao_fechar)
    
    def _criar_widgets(self):
        # Frame principal
        frame_principal = ctk.CTkFrame(self)
        frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
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
        frame_senha = ctk.CTkFrame(frame_principal)
        frame_senha.pack(fill="x", pady=10)
        
        # Campo para senha
        self.senha_entry = ctk.CTkEntry(
            frame_senha,
            placeholder_text="Nova senha",
            show="•",
            width=240
        )
        self.senha_entry.pack(side="left", padx=5)
        
        # Botão para mostrar/ocultar senha
        self.mostrar_senha_var = ctk.BooleanVar(value=False)
        btn_mostrar = ctk.CTkButton(
            frame_senha,
            text="👁",
            width=30,
            command=self._toggle_mostrar_senha
        )
        btn_mostrar.pack(side="left", padx=2)
        
        # Botão para gerar senha
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
        self.tamanho_var = ctk.IntVar(value=16)
        label_tamanho = ctk.CTkLabel(frame_opcoes, text="Tamanho:")
        label_tamanho.pack(side="left", padx=5)
        self.tamanho_entry = ctk.CTkEntry(
            frame_opcoes,
            width=50,
            textvariable=self.tamanho_var
        )
        self.tamanho_entry.pack(side="left", padx=5)
        
        # Checkboxes para opções de senha
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
            check = ctk.CTkCheckBox(
                frame_checks,
                text=texto,
                variable=var
            )
            check.pack(side="left", padx=5)
        
        # Frame para botões
        frame_botoes = ctk.CTkFrame(frame_principal)
        frame_botoes.pack(pady=20)
        
        # Botão salvar
        btn_salvar = ctk.CTkButton(
            frame_botoes,
            text="Salvar",
            command=self._salvar
        )
        btn_salvar.pack(side="left", padx=5)
        
        # Botão cancelar
        btn_cancelar = ctk.CTkButton(
            frame_botoes,
            text="Cancelar",
            command=self.destroy
        )
        btn_cancelar.pack(side="left", padx=5)
        
        # Botão copiar
        btn_copiar = ctk.CTkButton(
            frame_botoes,
            text="Copiar",
            command=self._copiar_senha
        )
        btn_copiar.pack(side="left", padx=5)
    
    def _preencher_dados_atuais(self):
        """Preenche os campos com os dados atuais da senha"""
        self.site_entry.insert(0, self.senha_atual.site)
        if self.senha_atual.username:
            self.username_entry.insert(0, self.senha_atual.username)
    
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
            self._mostrar_erro("Selecione pelo menos uma opção!")
            return
        
        try:
            tamanho = self.tamanho_var.get()
            if tamanho < 4:
                self._mostrar_erro("O tamanho mínimo é 4!")
                return
        except:
            self._mostrar_erro("Tamanho inválido!")
            return
        
        senha = ''.join(secrets.choice(caracteres) for _ in range(tamanho))
        self.senha_entry.delete(0, "end")
        self.senha_entry.insert(0, senha)
    
    def _copiar_senha(self):
        senha = self.senha_entry.get()
        if senha:
            pyperclip.copy(senha)
            self._mostrar_sucesso("Senha copiada para a área de transferência!")
        else:
            self._mostrar_erro("Nenhuma senha para copiar!")
    
    def _salvar(self):
        site = self.site_entry.get().strip()
        username = self.username_entry.get().strip()
        senha = self.senha_entry.get()
        
        if not site:
            self._mostrar_erro("O nome do site é obrigatório!")
            return
        
        # Se não houver alterações, mantém os valores atuais
        if not senha:
            senha = self.senha_atual.senha
        
        sucesso, mensagem = self.master.senha_controller.alterar_senha(
            id=self.senha_atual.id,
            site=site,
            senha=senha,
            username=username
        )
        
        if sucesso:
            self._mostrar_sucesso(mensagem)
            self.master._atualizar_lista()
            self.destroy()
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