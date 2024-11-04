from models.senha import Senha
from datetime import datetime
import logging

class SenhaController:
    def __init__(self, usuario_id):
        self.usuario_id = usuario_id
        self.logger = logging.getLogger('senha_controller')
    
    def adicionar_senha(self, site, senha, username=None):
        try:
            nova_senha = Senha(
                usuario_id=self.usuario_id,
                site=site,
                senha=senha,
                username=username
            )
            nova_senha.salvar()
            self.logger.info(f"Nova senha adicionada para o site: {site}")
            return True, "Senha adicionada com sucesso"
        except Exception as e:
            self.logger.error(f"Erro ao adicionar senha: {str(e)}")
            return False, f"Erro ao adicionar senha: {str(e)}"
    
    def alterar_senha(self, id, site=None, senha=None, username=None):
        try:
            senha_atual = Senha.buscar_por_id(id, self.usuario_id)
            if not senha_atual:
                self.logger.warning(f"Tentativa de alterar senha inexistente. ID: {id}")
                return False, "Senha não encontrada"
            
            if site:
                senha_atual.site = site
            if username is not None:  # Permite remover o username
                senha_atual.username = username
            if senha:
                senha_atual.senha = senha
            
            senha_atual.data_modificacao = datetime.now()
            senha_atual.salvar()
            
            self.logger.info(f"Senha alterada para o site: {senha_atual.site}")
            return True, "Senha alterada com sucesso"
        except Exception as e:
            self.logger.error(f"Erro ao alterar senha: {str(e)}")
            return False, f"Erro ao alterar senha: {str(e)}"
    
    def remover_senha(self, id):
        try:
            senha = Senha.buscar_por_id(id, self.usuario_id)
            if not senha:
                self.logger.warning(f"Tentativa de remover senha inexistente. ID: {id}")
                return False, "Senha não encontrada"
            
            if senha.deletar():
                self.logger.info(f"Senha removida para o site: {senha.site}")
                return True, "Senha removida com sucesso"
            
            return False, "Não foi possível remover a senha"
        except Exception as e:
            self.logger.error(f"Erro ao remover senha: {str(e)}")
            return False, f"Erro ao remover senha: {str(e)}"
    
    def listar_senhas(self, filtro=None):
        try:
            senhas = Senha.buscar_por_usuario(self.usuario_id)
            
            if filtro:
                filtro = filtro.lower()
                senhas = [
                    s for s in senhas 
                    if filtro in s.site.lower() or 
                    (s.username and filtro in s.username.lower())
                ]
            
            self.logger.info("Senhas listadas com sucesso")
            return True, senhas
        except Exception as e:
            self.logger.error(f"Erro ao listar senhas: {str(e)}")
            return False, f"Erro ao listar senhas: {str(e)}"
    
    def buscar_senha(self, id):
        try:
            senha = Senha.buscar_por_id(id, self.usuario_id)
            if not senha:
                self.logger.warning(f"Tentativa de buscar senha inexistente. ID: {id}")
                return False, "Senha não encontrada"
            
            self.logger.info(f"Senha encontrada para o site: {senha.site}")
            return True, senha
        except Exception as e:
            self.logger.error(f"Erro ao buscar senha: {str(e)}")
            return False, f"Erro ao buscar senha: {str(e)}"
    
    def verificar_duplicidade(self, site, username=None):
        """Verifica se já existe uma senha para o mesmo site/usuário"""
        try:
            senhas = Senha.buscar_por_usuario(self.usuario_id)
            for senha in senhas:
                if senha.site.lower() == site.lower():
                    if username:
                        if senha.username and senha.username.lower() == username.lower():
                            return True
                    else:
                        return True
            return False
        except Exception as e:
            self.logger.error(f"Erro ao verificar duplicidade: {str(e)}")
            return False