import customtkinter as ctk
from views.popups.adicionar_senha import AdicionarSenhaPopup
from views.popups.alterar_senha import AlterarSenhaPopup
from views.popups.trocar_tema import TrocarTemaPopup
from views.popups.backup import BackupPopup
from controllers.senha_controller import SenhaController
import pyperclip
import logging

class GerenciadorView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.senha_controller = SenhaController(self.master.auth_controller.usuario_atual.id)
        self.senhas_selecionadas = []
        self.logger = logging.getLogger('gerenciador_view')
        self.pack(fill="both", expand=True)
        self._criar_widgets()
        self._atualizar_lista()
        
        # Inicia verificação periódica de sessão
        self._verificar_sessao()
    
    def _criar_widgets(self):
        # Frame superior para título e pesquisa
        frame_superior = ctk.CTkFrame(self)
        frame_superior.pack(fill="x", padx=20, pady=10)
        
        # Título
        titulo = ctk.CTkLabel(
            frame_superior,
            text="GERENCIAMENTO DE SENHAS",
            font=("Roboto", 24, "bold")
        )
        titulo.pack(side="left", pady=10)
        
        # Frame de pesquisa
        frame_pesquisa = ctk.CTkFrame(self)
        frame_pesquisa.pack(fill="x", padx=20, pady=5)
        
        # Campo de pesquisa
        self.pesquisa_entry = ctk.CTkEntry(
            frame_pesquisa,
            placeholder_text="Pesquisar por site ou usuário...",
            width=300
        )
        self.pesquisa_entry.pack(side="left", padx=5)
        self.pesquisa_entry.bind("<KeyRelease>", self._filtrar_senhas)
        
        # Frame para botões de ação
        frame_acoes = ctk.CTkFrame(self)
        frame_acoes.pack(fill="x", padx=20, pady=5)
        
        # Botões de ação
        botoes = [
            ("Adicionar", self._abrir_adicionar, "#2E8B57"),        # Verde escuro
            ("Remover", self._remover_senha, "#B22222"),            # Vermelho mais escuro
            ("Alterar", self._abrir_alterar, "#3A506B"),            # Azul escuro
            ("Atualizar", self._atualizar_lista, "#2C2C2E"),        # Cinza escuro
            ("Copiar Senha", lambda: self._copiar_dado('senha'), "#2C2C2E"), # Cinza escuro
            ("Copiar Usuário", lambda: self._copiar_dado('usuario'), "#2C2C2E"), # Cinza escuro
            ("Backup", self._abrir_backup, "#2C2C2E"), # Cinza escuro            
            ("Temas", self._abrir_temas, "#2C2C2E"), # Cinza escuro               
            ("Voltar", self._voltar_login, "#8E7CC3")  # Cinza escuro 
        ]
        
        for texto, comando, cor in botoes:
            btn = ctk.CTkButton(
                frame_acoes,
                text=texto,
                command=comando,
                width=100,
                fg_color=cor
            )
            btn.pack(side="left", padx=5)
        
        # Frame para a tabela de senhas
        self.frame_tabela = ctk.CTkFrame(self)
        self.frame_tabela.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Criar cabeçalho da tabela
        self._criar_cabecalho()
        
        # Frame para lista de senhas
        self.frame_lista = ctk.CTkScrollableFrame(self.frame_tabela)
        self.frame_lista.pack(fill="both", expand=True)
    
    def _criar_cabecalho(self):
        frame_header = ctk.CTkFrame(self.frame_tabela)
        frame_header.pack(fill="x", padx=5, pady=5)
        
        colunas = [
            ("Site", 2),
            ("Usuário", 2),
            ("Última Modificação", 1)
        ]
        
        for texto, peso in colunas:
            frame_coluna = ctk.CTkFrame(frame_header)
            frame_coluna.pack(side="left", expand=True, fill="x", padx=2)
            
            label = ctk.CTkLabel(
                frame_coluna,
                text=texto,
                font=("Roboto", 12, "bold"),
                anchor="w"
            )
            label.pack(fill="x", padx=5, pady=5)
    
    def _criar_item_senha(self, senha, frame):
        frame_item = ctk.CTkFrame(frame)
        frame_item.pack(fill="x", padx=5, pady=2)
        
        # Adiciona um evento de clique no frame principal
        frame_item.bind("<Button-1>", lambda e, s=senha, f=frame_item: self._selecionar_item(s, f))
        
        # Site
        frame_site = ctk.CTkFrame(frame_item, fg_color="transparent")
        frame_site.pack(side="left", expand=True, fill="x", padx=2)
        label_site = ctk.CTkLabel(
            frame_site,
            text=senha.site,
            anchor="w"
        )
        label_site.pack(fill="x", padx=5)
        
        # Usuário
        frame_usuario = ctk.CTkFrame(frame_item, fg_color="transparent")
        frame_usuario.pack(side="left", expand=True, fill="x", padx=2)
        label_usuario = ctk.CTkLabel(
            frame_usuario,
            text=senha.username or "",
            anchor="w"
        )
        label_usuario.pack(fill="x", padx=5)
        
        # Data de modificação
        frame_data = ctk.CTkFrame(frame_item, fg_color="transparent")
        frame_data.pack(side="left", expand=True, fill="x", padx=2)
        
        # Verifica se data_modificacao é string ou datetime
        if hasattr(senha.data_modificacao, 'strftime'):
            data_texto = senha.data_modificacao.strftime("%d/%m/%Y %H:%M")
        else:
            data_texto = str(senha.data_modificacao)  # Usa a string diretamente
            
        label_data = ctk.CTkLabel(
            frame_data,
            text=data_texto,
            anchor="w"
        )
        label_data.pack(fill="x", padx=5)
        
        # Bind de clique para todos os elementos
        for widget in [frame_site, frame_usuario, frame_data,
                      label_site, label_usuario, label_data]:
            widget.bind("<Button-1>", lambda e, s=senha, f=frame_item: self._selecionar_item(s, f))
    
    def _selecionar_item(self, senha, frame):
        if senha in self.senhas_selecionadas:
            self.senhas_selecionadas.remove(senha)
            frame.configure(fg_color=("gray90", "gray13"))
        else:
            self.senhas_selecionadas = [senha]  # Seleciona apenas um
            for child in self.frame_lista.winfo_children():
                child.configure(fg_color=("gray90", "gray13"))
            frame.configure(fg_color=("gray70", "gray30"))
    
    def _atualizar_lista(self):
        try:
            # Limpa a seleção atual
            self.senhas_selecionadas = []
            
            # Busca as senhas antes de limpar a lista atual
            sucesso, resultado = self.senha_controller.listar_senhas()
            
            if not sucesso:
                self._mostrar_erro("Erro ao carregar senhas")
                self.logger.error("Falha ao buscar senhas do banco de dados")
                return
                
            # Se a busca foi bem sucedida, então limpa e atualiza a lista
            for widget in self.frame_lista.winfo_children():
                widget.destroy()
            
            # Limpa o campo de pesquisa
            self.pesquisa_entry.delete(0, 'end')
            
            # Exibe as senhas
            if resultado:  # Verifica se há senhas para exibir
                for senha in resultado:
                    self._criar_item_senha(senha, self.frame_lista)
                self.logger.info(f"Lista atualizada com {len(resultado)} senhas")
            else:
                # Se não houver senhas, exibe uma mensagem na lista
                label = ctk.CTkLabel(
                    self.frame_lista,
                    text="Nenhuma senha cadastrada",
                    font=("Roboto", 12),
                    anchor="center"
                )
                label.pack(pady=20)
                self.logger.info("Lista atualizada - nenhuma senha encontrada")
                
        except Exception as e:
            self.logger.error(f"Erro ao atualizar lista: {str(e)}")
            self._mostrar_erro(f"Erro ao atualizar lista: {str(e)}")
    
    def _filtrar_senhas(self, event=None):
        try:
            filtro = self.pesquisa_entry.get()
            sucesso, resultado = self.senha_controller.listar_senhas(filtro)
            
            # Limpa a lista atual
            for widget in self.frame_lista.winfo_children():
                widget.destroy()
            
            # Exibe resultados filtrados
            if sucesso:
                for senha in resultado:
                    self._criar_item_senha(senha, self.frame_lista)
                
        except Exception as e:
            self.logger.error(f"Erro ao filtrar senhas: {str(e)}")
            self._mostrar_erro("Erro ao filtrar senhas")
    
    def _copiar_dado(self, tipo):
        if not self.senhas_selecionadas:
            self._mostrar_erro("Selecione uma senha primeiro!")
            return
        
        try:
            senha = self.senhas_selecionadas[0]
            if tipo == 'senha':
                pyperclip.copy(senha.senha)
            else:
                pyperclip.copy(senha.username or '')
            
            self._mostrar_sucesso(f"{tipo.title()} copiado para a área de transferência!")
            self.logger.info(f"{tipo.title()} copiado para área de transferência")
            
        except Exception as e:
            self.logger.error(f"Erro ao copiar {tipo}: {str(e)}")
            self._mostrar_erro(f"Erro ao copiar {tipo}")
    
    def _abrir_adicionar(self):
        AdicionarSenhaPopup(self)
    
    def _remover_senha(self):
        if not self.senhas_selecionadas:
            self._mostrar_erro("Selecione uma senha para remover!")
            return
        
        try:
            senha = self.senhas_selecionadas[0]
            sucesso, mensagem = self.senha_controller.remover_senha(senha.id)
            
            if sucesso:
                self._mostrar_sucesso(mensagem)
                self._atualizar_lista()
            else:
                self._mostrar_erro(mensagem)
                
        except Exception as e:
            self.logger.error(f"Erro ao remover senha: {str(e)}")
            self._mostrar_erro("Erro ao remover senha")
    
    def _abrir_alterar(self):
        if not self.senhas_selecionadas:
            self._mostrar_erro("Selecione uma senha para alterar!")
            return
        
        AlterarSenhaPopup(self, self.senhas_selecionadas[0])
    
    def _abrir_backup(self):
        BackupPopup(self)
    
    def _abrir_temas(self):
        TrocarTemaPopup(self)
    
    def _voltar_login(self):
        from views.login_view import LoginView
        self.master.auth_controller.logout()
        self.destroy()
        LoginView(self.master)
    
    def _verificar_sessao(self):
        """Verifica periodicamente se a sessão ainda está ativa"""
        if not self.master.auth_controller.verificar_sessao_ativa():
            self._voltar_login()
            return
        
        # Agenda próxima verificação em 1 minuto
        self.after(60000, self._verificar_sessao)
    
    def _mostrar_erro(self, mensagem):
        erro = ctk.CTkToplevel(self)
        erro.title("Erro")
        erro.geometry("300x150")
        erro.transient(self)  # Define a janela principal como pai
        erro.grab_set()       # Força o foco na janela de erro
        
        # Centraliza a janela
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
        sucesso.transient(self)  # Define a janela principal como pai
        sucesso.grab_set()       # Força o foco na janela de sucesso
        
        # Centraliza a janela
        sucesso.update_idletasks()
        x = (sucesso.winfo_screenwidth() - sucesso.winfo_width()) // 2
        y = (sucesso.winfo_screenheight() - sucesso.winfo_height()) // 2
        sucesso.geometry(f"+{x}+{y}")
        
        label = ctk.CTkLabel(sucesso, text=mensagem)
        label.pack(pady=20)
        
        btn = ctk.CTkButton(sucesso, text="OK", command=sucesso.destroy)
        btn.pack(pady=10)