from datetime import datetime, timedelta
from utils.database import Database

class PoliticaSenha:
    def __init__(self):
        self.db = Database()
        self.max_idade_senha = 90  # dias
        self.min_caracteres = 8
        self.requer_maiuscula = True
        self.requer_minuscula = True
        self.requer_numero = True
        self.requer_especial = True
        self.historico_senhas = 5  # últimas senhas que não podem ser reutilizadas
    
    def verificar_expiracao(self, usuario_id) -> bool:
        """Verifica se a senha do usuário expirou"""
        with self.db.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT ultima_troca_senha 
                FROM usuarios 
                WHERE id = ?
            ''', (usuario_id,))
            
            resultado = cursor.fetchone()
            if not resultado or not resultado[0]:
                return True
                
            ultima_troca = datetime.strptime(resultado[0], '%Y-%m-%d %H:%M:%S')
            return datetime.now() - ultima_troca > timedelta(days=self.max_idade_senha)
    
    def verificar_historico(self, usuario_id, nova_senha) -> bool:
        """Verifica se a senha já foi usada recentemente"""
        with self.db.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT senha_hash 
                FROM historico_senhas 
                WHERE usuario_id = ? 
                ORDER BY data_modificacao DESC 
                LIMIT ?
            ''', (usuario_id, self.historico_senhas))
            
            for senha_antiga in cursor.fetchall():
                if self.crypto.verificar_senha(nova_senha, senha_antiga[0]):
                    return False
            return True
