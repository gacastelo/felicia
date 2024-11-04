from datetime import datetime
from utils.database import Database
import logging

logger = logging.getLogger('gerenciador_senhas')

class NotificacaoService:
    def __init__(self):
        self.db = Database()
        self._criar_tabela()
    
    def _criar_tabela(self):
        with self.db.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notificacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER NOT NULL,
                    tipo TEXT NOT NULL,
                    mensagem TEXT NOT NULL,
                    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
                    lida BOOLEAN DEFAULT 0,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                )
            ''')
    
    def adicionar_notificacao(self, usuario_id, tipo, mensagem):
        try:
            with self.db.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO notificacoes (usuario_id, tipo, mensagem)
                    VALUES (?, ?, ?)
                ''', (usuario_id, tipo, mensagem))
                logger.info(f"Notificação criada para usuário {usuario_id}: {tipo}")
                return True
        except Exception as e:
            logger.error(f"Erro ao criar notificação: {str(e)}")
            return False
    
    def get_notificacoes_pendentes(self, usuario_id):
        with self.db.conectar() as conn:
            cursor = conn.cursor()
            return cursor.execute('''
                SELECT id, tipo, mensagem, data_criacao 
                FROM notificacoes 
                WHERE usuario_id = ? AND lida = 0
                ORDER BY data_criacao DESC
            ''', (usuario_id,)).fetchall()
    
    def marcar_como_lida(self, notificacao_id):
        with self.db.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE notificacoes 
                SET lida = 1 
                WHERE id = ?
            ''', (notificacao_id,))
