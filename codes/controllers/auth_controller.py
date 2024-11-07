import hashlib
import secrets
from datetime import datetime, timedelta
from models.usuario import Usuario
import logging

class AuthController:
    def __init__(self):
        self.usuario_atual = None
        self.tempo_ultima_atividade = datetime.now()
        self.logger = logging.getLogger('auth_controller')
    
    def login(self, username, password):
        try:
            usuario = Usuario.buscar_por_username(username)
            
            if not usuario:
                self.logger.warning(f"Tentativa de login com usuário inexistente: {username}")
                return False, "Usuário não encontrado"
            
            # Verifica se o usuário está bloqueado
            if usuario.bloqueado_ate and usuario.bloqueado_ate > datetime.now():
                self.logger.warning(f"Tentativa de login de usuário bloqueado: {username}")
                return False, "Usuário bloqueado. Tente novamente mais tarde"
            
            # Gera o hash da senha fornecida com o salt do usuário
            senha_hash = self._gerar_hash_senha(password, usuario.salt)
            
            if senha_hash != usuario.password_hash:
                # Incrementa tentativas de login
                usuario.tentativas_login += 1
                if usuario.tentativas_login >= 3:
                    usuario.bloqueado_ate = datetime.now() + timedelta(minutes=30)
                    self.logger.warning(f"Usuário bloqueado após 3 tentativas: {username}")
                usuario.salvar()
                return False, "Senha incorreta"
            
            # Login bem sucedido - reseta contadores
            usuario.tentativas_login = 0
            usuario.ultimo_acesso = datetime.now()
            usuario.salvar()
            
            self.usuario_atual = usuario
            self.tempo_ultima_atividade = datetime.now()
            self.logger.info(f"Login bem sucedido: {username}")
            return True, "Login realizado com sucesso"
            
        except Exception as e:
            self.logger.error(f"Erro no login: {str(e)}")
            return False, f"Erro ao realizar login: {str(e)}"
    
    def cadastrar(self, username, password):
        try:
            if Usuario.buscar_por_username(username):
                self.logger.warning(f"Tentativa de cadastro de usuário existente: {username}")
                return False, "Nome de usuário já existe"
            
            # Gera um salt aleatório
            salt = secrets.token_hex(16)
            # Gera o hash da senha
            password_hash = self._gerar_hash_senha(password, salt)
            
            novo_usuario = Usuario(
                username=username,
                password_hash=password_hash,
                salt=salt,
                data_criacao=datetime.now(),
                is_admin=False
            )
            
            novo_usuario.salvar()
            self.logger.info(f"Novo usuário cadastrado: {username}")
            return True, "Usuário cadastrado com sucesso"
            
        except Exception as e:
            self.logger.error(f"Erro no cadastro: {str(e)}")
            return False, f"Erro ao cadastrar usuário: {str(e)}"
    
    def _gerar_hash_senha(self, senha, salt):
        return hashlib.sha256((senha + salt).encode()).hexdigest()
    
    def verificar_sessao_ativa(self):
        if not self.usuario_atual:
            return False
        
        tempo_inativo = (datetime.now() - self.tempo_ultima_atividade).seconds
        if tempo_inativo > 900:  # 15 minutos
            self.logger.info(f"Sessão expirada por inatividade: {self.usuario_atual.username}")
            self.logout()
            return False
        
        self.tempo_ultima_atividade = datetime.now()
        return True
    
    def logout(self):
        if self.usuario_atual:
            self.logger.info(f"Logout realizado: {self.usuario_atual.username}")
            self.usuario_atual = None
            self.tempo_ultima_atividade = None