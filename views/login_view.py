from views.base_view import BaseView
import customtkinter as ctk

class LoginView(BaseView):
    def __init__(self, master):
        super().__init__(master)
        self._criar_widgets()
    
    def _criar_widgets(self):
        # Frame central
        frame_central = ctk.CTkFrame(self)
        frame_central.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        titulo = ctk.CTkLabel(
            frame_central,
            text="LOGIN",
            font=("Roboto", 24, "bold")
        )
        titulo.pack(pady=20)
        
        # Subtítulo
        subtitulo = ctk.CTkLabel(
            frame_central,
            text="Informe seu nome de usuário e senha para continuar",
            font=("Roboto", 12)
        )
        subtitulo.pack(pady=10)
        
        # Campo de usuário
        self.username_entry = ctk.CTkEntry(
            frame_central,
            placeholder_text="Nome de usuário",
            width=300
        )
        self.username_entry.pack(pady=10)
        
        # Campo de senha
        self.password_entry = ctk.CTkEntry(
            frame_central,
            placeholder_text="Senha",
            show="•",
            width=300
        )
        self.password_entry.pack(pady=10)
        
        # Frame para botões
        frame_botoes = ctk.CTkFrame(frame_central)
        frame_botoes.pack(pady=20)
        
        # Botão de login
        btn_login = ctk.CTkButton(
            frame_botoes,
            text="Entrar",
            command=self._fazer_login
        )
        btn_login.pack(side="left", padx=5)
        
        # Botão de cadastro
        btn_cadastro = ctk.CTkButton(
            frame_botoes,
            text="Cadastrar",
            command=self._abrir_cadastro
        )
        btn_cadastro.pack(side="left", padx=5)
        
        # Botão de sair
        btn_sair = ctk.CTkButton(
            frame_botoes,
            text="Sair",
            command=self.master.quit
        )
        btn_sair.pack(side="left", padx=5)
        
        # Bind Enter para login
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self._fazer_login())
    
    def _fazer_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            self._mostrar_erro("Preencha todos os campos!")
            return
        
        sucesso, mensagem = self.master.auth_controller.login(username, password)
        
        if sucesso:
            self._abrir_gerenciador()
        else:
            self._mostrar_erro(mensagem)
            self.password_entry.delete(0, "end")
    
    def _abrir_cadastro(self):
        from views.cadastro_view import CadastroView
        self.destroy()
        CadastroView(self.master)
    
    def _abrir_gerenciador(self):
        from views.gerenciador_view import GerenciadorView
        self.destroy()
        GerenciadorView(self.master)
    
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