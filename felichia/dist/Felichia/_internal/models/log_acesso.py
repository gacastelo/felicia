from datetime import datetime
from utils.database import Database

class LogAcesso:
    def __init__(self, usuario_id, acao, ip=None, detalhes=None):
        self.usuario_id = usuario_id
        self.acao = acao
        self.ip = ip
        self.detalhes = detalhes
        self.db = Database()
    
    def salvar(self):
        with self.db.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO logs_acesso (usuario_id, acao, ip, detalhes)
                VALUES (?, ?, ?, ?)
            ''', (self.usuario_id, self.acao, self.ip, self.detalhes))
            return True
