from utils.database import Database
from datetime import datetime
import logging

class Usuario:
    def __init__(self, username, password_hash, salt, data_criacao=None, 
                 ultimo_acesso=None, is_admin=False, id=None, 
                 tentativas_login=0, bloqueado_ate=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.salt = salt
        self.data_criacao = data_criacao or datetime.now()
        self.ultimo_acesso = ultimo_acesso
        self.is_admin = is_admin
        self.tentativas_login = tentativas_login
        self.bloqueado_ate = bloqueado_ate
        self.logger = logging.getLogger('usuario_model')
    
    def salvar(self):
        try:
            db = Database()
            with db.conectar() as conn:
                cursor = conn.cursor()
                
                if self.id is None:
                    # Inserir novo usuário
                    cursor.execute('''
                        INSERT INTO usuarios (
                            username, password_hash, salt, data_criacao,
                            ultimo_acesso, is_admin, tentativas_login, bloqueado_ate
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        self.username, self.password_hash, self.salt,
                        self.data_criacao, self.ultimo_acesso, self.is_admin,
                        self.tentativas_login, self.bloqueado_ate
                    ))
                    self.id = cursor.lastrowid
                    self.logger.info(f"Novo usuário criado: {self.username}")
                else:
                    # Atualizar usuário existente
                    cursor.execute('''
                        UPDATE usuarios SET
                            username=?, password_hash=?, salt=?,
                            ultimo_acesso=?, is_admin=?,
                            tentativas_login=?, bloqueado_ate=?
                        WHERE id=?
                    ''', (
                        self.username, self.password_hash, self.salt,
                        self.ultimo_acesso, self.is_admin,
                        self.tentativas_login, self.bloqueado_ate,
                        self.id
                    ))
                    self.logger.info(f"Usuário atualizado: {self.username}")
                
        except Exception as e:
            self.logger.error(f"Erro ao salvar usuário: {str(e)}")
            raise
    
    @staticmethod
    def buscar_por_username(username):
        try:
            db = Database()
            with db.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, username, password_hash, salt, data_criacao,
                           ultimo_acesso, is_admin, tentativas_login, bloqueado_ate
                    FROM usuarios WHERE username = ?
                ''', (username,))
                
                resultado = cursor.fetchone()
                if resultado:
                    return Usuario(
                        id=resultado[0],
                        username=resultado[1],
                        password_hash=resultado[2],
                        salt=resultado[3],
                        data_criacao=resultado[4],
                        ultimo_acesso=resultado[5],
                        is_admin=resultado[6],
                        tentativas_login=resultado[7],
                        bloqueado_ate=resultado[8]
                    )
            return None
            
        except Exception as e:
            logging.error(f"Erro ao buscar usuário: {str(e)}")
            raise
    
    @staticmethod
    def buscar_todos():
        try:
            db = Database()
            with db.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM usuarios')
                
                usuarios = []
                for row in cursor.fetchall():
                    usuarios.append(Usuario(
                        id=row[0],
                        username=row[1],
                        password_hash=row[2],
                        salt=row[3],
                        data_criacao=row[4],
                        ultimo_acesso=row[5],
                        is_admin=row[6],
                        tentativas_login=row[7],
                        bloqueado_ate=row[8]
                    ))
                return usuarios
                
        except Exception as e:
            logging.error(f"Erro ao buscar todos os usuários: {str(e)}")
            raise