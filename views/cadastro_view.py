import customtkinter as ctk
import re

class CadastroView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True)
        self._criar_widgets()
    
    def _criar_widgets(self):
        # Frame central
        frame_central = ctk.CTkFrame(self)
        frame_central.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        titulo = ctk.CTkLabel(
            frame_central,
            text="CADASTRO",
            font=("Roboto", 24, "bold")
        )
        titulo.pack(pady=20)
        
        # Subtítulo
        subtitulo = ctk.CTkLabel(
            frame_central,
            text="Crie seu nome de usuário e senha para continuar",
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
        
        # Campo de confirmação de senha
        self.confirm_password_entry = ctk.CTkEntry(
            frame_central,
            placeholder_text="Confirme a senha",
            show="•",
            width=300
        )
        self.confirm_password_entry.pack(pady=10)
        
        # Indicadores de força da senha
        self.frame_forca = ctk.CTkFrame(frame_central)
        self.frame_forca.pack(pady=10)
        
        self.label_forca = ctk.CTkLabel(
            self.frame_forca,
            text="Força da senha:",
            font=("Roboto", 11)
        )
        self.label_forca.pack(side="left", padx=5)
        
        self.barra_forca = ctk.CTkProgressBar(
            self.frame_forca,
            width=200,
            height=10
        )
        self.barra_forca.pack(side="left", padx=5)
        self.barra_forca.set(0)
        
        # Requisitos da senha
        frame_requisitos = ctk.CTkFrame(frame_central)
        frame_requisitos.pack(pady=5)
        
        requisitos = [
            "Mínimo 8 caracteres",
            "Letra maiúscula",
            "Letra minúscula",
            "Número",
            "Caractere especial"
        ]
        
        self.labels_requisitos = {}
        for req in requisitos:
            label = ctk.CTkLabel(
                frame_requisitos,
                text="✗ " + req,
                font=("Roboto", 10),
                text_color="gray60"
            )
            label.pack(anchor="w", padx=5)
            self.labels_requisitos[req] = label
        
        # Frame para botões
        frame_botoes = ctk.CTkFrame(frame_central)
        frame_botoes.pack(pady=20)
        
        # Botão de cadastrar
        btn_cadastrar = ctk.CTkButton(
            frame_botoes,
            text="Cadastrar",
            command=self._fazer_cadastro
        )
        btn_cadastrar.pack(side="left", padx=5)
        
        # Botão de voltar
        btn_voltar = ctk.CTkButton(
            frame_botoes,
            text="Voltar",
            command=self._voltar_login
        )
        btn_voltar.pack(side="left", padx=5)
        
        # Bind para verificar força da senha
        self.password_entry.bind("<KeyRelease>", self._verificar_forca_senha)
    
    def _verificar_forca_senha(self, event=None):
        senha = self.password_entry.get()
        pontuacao = 0
        max_pontos = 5
        
        # Verifica cada requisito
        requisitos = {
            "Mínimo 8 caracteres": len(senha) >= 8,
            "Letra maiúscula": bool(re.search(r'[A-Z]', senha)),
            "Letra minúscula": bool(re.search(r'[a-z]', senha)),
            "Número": bool(re.search(r'\d', senha)),
            "Caractere especial": bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', senha))
        }
        
        # Atualiza os indicadores visuais
        for req, atende in requisitos.items():
            label = self.labels_requisitos[req]
            if atende:
                label.configure(text="✓ " + req, text_color="green")
                pontuacao += 1
            else:
                label.configure(text="✗ " + req, text_color="gray60")
        
        # Atualiza a barra de progresso
        self.barra_forca.set(pontuacao / max_pontos)
        
        # Define a cor da barra baseado na força
        if pontuacao <= 2:
            self.barra_forca.configure(progress_color="red")
        elif pontuacao <= 3:
            self.barra_forca.configure(progress_color="yellow")
        else:
            self.barra_forca.configure(progress_color="green")
    
    def _fazer_cadastro(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        # Validações básicas
        if not username or not password or not confirm_password:
            self._mostrar_erro("Todos os campos são obrigatórios!")
            return
        
        if password != confirm_password:
            self._mostrar_erro("As senhas não coincidem!")
            return
        
        if len(password) < 8:
            self._mostrar_erro("A senha deve ter pelo menos 8 caracteres!")
            return
        
        # Verifica requisitos mínimos de senha
        if not all([
            re.search(r'[A-Z]', password),
            re.search(r'[a-z]', password),
            re.search(r'\d', password),
            re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
        ]):
            self._mostrar_erro("A senha não atende aos requisitos mínimos!")
            return
        
        # Tenta cadastrar o usuário
        sucesso, mensagem = self.master.auth_controller.cadastrar(username, password)
        
        if sucesso:
            self._mostrar_sucesso("Cadastro realizado com sucesso!")
            self.master.after(2000, self._voltar_login)
        else:
            self._mostrar_erro(mensagem)
    
    def _voltar_login(self):
        from views.login_view import LoginView
        self.destroy()
        LoginView(self.master)
    
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