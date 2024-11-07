from utils.database import Database

class Configuracao:
    def __init__(self, usuario_id):
        self.usuario_id = usuario_id
        self.db = Database()
        self.carregar()
    
    def carregar(self):
        with self.db.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT tempo_sessao, tempo_expiracao_senha, tema,
                       backup_automatico, intervalo_backup
                FROM configuracoes
                WHERE usuario_id = ?
            ''', (self.usuario_id,))
            
            resultado = cursor.fetchone()
            if resultado:
                self.tempo_sessao = resultado[0]
                self.tempo_expiracao_senha = resultado[1]
                self.tema = resultado[2]
                self.backup_automatico = resultado[3]
                self.intervalo_backup = resultado[4]
            else:
                # Criar configurações padrão
                self.criar_padrao()
    
    def criar_padrao(self):
        with self.db.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO configuracoes (usuario_id)
                VALUES (?)
            ''', (self.usuario_id,))
            self.carregar()
