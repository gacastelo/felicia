from utils.database import Database
from datetime import datetime
from utils.criptografia import Criptografia
import logging

class Senha:
    def __init__(self, usuario_id, site, senha, username=None, id=None,
                 data_criacao=None, data_modificacao=None):
        self.id = id
        self.usuario_id = usuario_id
        self.site = site
        self.username = username
        self.senha_criptografada = None
        self.senha_descriptografada = senha
        self.data_criacao = data_criacao or datetime.now()
        self.data_modificacao = data_modificacao or datetime.now()
        self.cripto = Criptografia()
        self.logger = logging.getLogger('senha_model')
    
    def salvar(self):
        try:
            if not self.senha_criptografada:
                self.senha_criptografada = self.cripto.criptografar(self.senha_descriptografada)
            
            db = Database()
            with db.conectar() as conn:
                cursor = conn.cursor()
                
                if self.id is None:
                    # Inserir nova senha
                    cursor.execute('''
                        INSERT INTO senhas (
                            usuario_id, site, username, senha_criptografada,
                            data_criacao, data_modificacao
                        ) VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        self.usuario_id, self.site, self.username,
                        self.senha_criptografada, self.data_criacao,
                        self.data_modificacao
                    ))
                    self.id = cursor.lastrowid
                    self.logger.info(f"Nova senha criada para o site: {self.site}")
                else:
                    # Salvar senha antiga no histórico
                    senha_antiga = Senha.buscar_por_id(self.id, self.usuario_id)
                    if senha_antiga:
                        cursor.execute('''
                            INSERT INTO historico_senhas (
                                senha_id, senha_antiga, modificado_por
                            ) VALUES (?, ?, ?)
                        ''', (
                            self.id, senha_antiga.senha_criptografada,
                            self.usuario_id
                        ))
                    
                    # Atualizar senha existente
                    cursor.execute('''
                        UPDATE senhas SET
                            site=?, username=?, senha_criptografada=?,
                            data_modificacao=?
                        WHERE id=? AND usuario_id=?
                    ''', (
                        self.site, self.username, self.senha_criptografada,
                        datetime.now(), self.id, self.usuario_id
                    ))
                    self.logger.info(f"Senha atualizada para o site: {self.site}")
        
        except Exception as e:
            self.logger.error(f"Erro ao salvar senha: {str(e)}")
            raise
    
    def deletar(self):
        try:
            if not self.id:
                return False
            
            db = Database()
            with db.conectar() as conn:
                cursor = conn.cursor()
                
                # Salvar no histórico antes de deletar
                cursor.execute('''
                    INSERT INTO historico_senhas (
                        senha_id, senha_antiga, modificado_por
                    ) VALUES (?, ?, ?)
                ''', (self.id, self.senha_criptografada, self.usuario_id))
                
                # Deletar a senha
                cursor.execute('''
                    DELETE FROM senhas
                    WHERE id=? AND usuario_id=?
                ''', (self.id, self.usuario_id))
                
                self.logger.info(f"Senha deletada para o site: {self.site}")
                return cursor.rowcount > 0
        
        except Exception as e:
            self.logger.error(f"Erro ao deletar senha: {str(e)}")
            raise
    
    @property
    def senha(self):
        if self.senha_descriptografada:
            return self.senha_descriptografada
        
        if self.senha_criptografada:
            self.senha_descriptografada = self.cripto.descriptografar(
                self.senha_criptografada
            )
            return self.senha_descriptografada
        return None
    
    @senha.setter
    def senha(self, valor):
        self.senha_descriptografada = valor
        self.senha_criptografada = None
    
    @staticmethod
    def buscar_por_usuario(usuario_id):
        try:
            db = Database()
            with db.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, usuario_id, site, username, senha_criptografada,
                           data_criacao, data_modificacao
                    FROM senhas WHERE usuario_id = ?
                    ORDER BY site
                ''', (usuario_id,))
                
                senhas = []
                for row in cursor.fetchall():
                    senha = Senha(
                        id=row[0],
                        usuario_id=row[1],
                        site=row[2],
                        username=row[3],
                        senha='',  # Será descriptografada apenas quando necessário
                        data_criacao=row[5],
                        data_modificacao=row[6]
                    )
                    senha.senha_criptografada = row[4]
                    senhas.append(senha)
                
                return senhas
        
        except Exception as e:
            logging.error(f"Erro ao buscar senhas do usuário: {str(e)}")
            raise
    
    @staticmethod
    def buscar_por_id(id, usuario_id):
        try:
            db = Database()
            with db.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, usuario_id, site, username, senha_criptografada,
                           data_criacao, data_modificacao
                    FROM senhas WHERE id = ? AND usuario_id = ?
                ''', (id, usuario_id))
                
                row = cursor.fetchone()
                if row:
                    senha = Senha(
                        id=row[0],
                        usuario_id=row[1],
                        site=row[2],
                        username=row[3],
                        senha='',
                        data_criacao=row[5],
                        data_modificacao=row[6]
                    )
                    senha.senha_criptografada = row[4]
                    return senha
            return None
        
        except Exception as e:
            logging.error(f"Erro ao buscar senha por ID: {str(e)}")
            raise