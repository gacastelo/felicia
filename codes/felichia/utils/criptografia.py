from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
from pathlib import Path
import logging

class Criptografia:
    def __init__(self):
        self.logger = logging.getLogger('criptografia')
        self.chave = self._carregar_ou_criar_chave()
        self.fernet = Fernet(self.chave)
    
    def _carregar_ou_criar_chave(self):
        """Carrega a chave existente ou cria uma nova"""
        try:
            chave_path = Path("data/chave.key")
            
            if chave_path.exists():
                with open(chave_path, "rb") as arquivo_chave:
                    self.logger.info("Chave de criptografia carregada")
                    return arquivo_chave.read()
            
            # Se não existir, cria uma nova chave
            chave_path.parent.mkdir(exist_ok=True)
            
            # Gera um salt aleatório
            salt = os.urandom(16)
            
            # Usa PBKDF2 para derivar uma chave segura
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            
            # Gera uma chave base64 compatível com Fernet
            chave = base64.urlsafe_b64encode(kdf.derive(b"senha_mestra"))
            
            # Salva a chave
            with open(chave_path, "wb") as arquivo_chave:
                arquivo_chave.write(chave)
            
            self.logger.info("Nova chave de criptografia criada")
            return chave
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar/criar chave: {str(e)}")
            raise
    
    def criptografar(self, texto):
        """Criptografa um texto"""
        try:
            if not texto:
                return None
            
            # Converte para bytes se for string
            if isinstance(texto, str):
                texto = texto.encode()
            
            # Criptografa e retorna em base64
            return self.fernet.encrypt(texto).decode()
            
        except Exception as e:
            self.logger.error(f"Erro ao criptografar: {str(e)}")
            raise
    
    def descriptografar(self, texto_criptografado):
        """Descriptografa um texto"""
        try:
            if not texto_criptografado:
                return None
            
            # Converte de base64 e descriptografa
            if isinstance(texto_criptografado, str):
                texto_criptografado = texto_criptografado.encode()
            
            return self.fernet.decrypt(texto_criptografado).decode()
            
        except Exception as e:
            self.logger.error(f"Erro ao descriptografar: {str(e)}")
            return None
    
    def alterar_senha_mestra(self, nova_senha):
        """Altera a senha mestra e recriptografa todas as senhas"""
        try:
            from models.senha import Senha
            from models.usuario import Usuario
            
            # Gera nova chave com a nova senha
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            nova_chave = base64.urlsafe_b64encode(kdf.derive(nova_senha.encode()))
            
            # Cria nova instância do Fernet com a nova chave
            novo_fernet = Fernet(nova_chave)
            
            # Busca todas as senhas
            usuarios = Usuario.buscar_todos()
            for usuario in usuarios:
                senhas = Senha.buscar_por_usuario(usuario.id)
                for senha in senhas:
                    # Descriptografa com a chave antiga
                    texto_plano = self.descriptografar(senha.senha_criptografada)
                    if texto_plano:
                        # Criptografa com a nova chave
                        senha.senha_criptografada = novo_fernet.encrypt(
                            texto_plano.encode()
                        ).decode()
                        senha.salvar()
            
            # Salva a nova chave
            self.chave = nova_chave
            self.fernet = novo_fernet
            
            chave_path = Path("data/chave.key")
            with open(chave_path, "wb") as arquivo_chave:
                arquivo_chave.write(nova_chave)
            
            self.logger.info("Senha mestra alterada com sucesso")
            return True, "Senha mestra alterada com sucesso"
            
        except Exception as e:
            self.logger.error(f"Erro ao alterar senha mestra: {str(e)}")
            return False, f"Erro ao alterar senha mestra: {str(e)}"