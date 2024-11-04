import sqlite3
from pathlib import Path
import logging

class Database:
    def __init__(self):
        self.db_path = Path("data/senhas.db")
        self.db_path.parent.mkdir(exist_ok=True)
        self.logger = logging.getLogger('database')
    
    def conectar(self):
        """Estabelece conexão com o banco de dados"""
        try:
            return sqlite3.connect(self.db_path)
        except Exception as e:
            self.logger.error(f"Erro ao conectar ao banco de dados: {str(e)}")
            raise
    
    def criar_tabelas(self):
        """Cria as tabelas necessárias no banco de dados"""
        try:
            with self.conectar() as conn:
                cursor = conn.cursor()
                
                # Tabela de Usuários
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        salt TEXT NOT NULL,
                        data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
                        ultimo_acesso DATETIME,
                        is_admin BOOLEAN DEFAULT 0,
                        tentativas_login INTEGER DEFAULT 0,
                        bloqueado_ate DATETIME
                    )
                ''')
                
                # Tabela de Senhas
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS senhas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        usuario_id INTEGER NOT NULL,
                        site TEXT NOT NULL,
                        username TEXT,
                        senha_criptografada TEXT NOT NULL,
                        data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
                        data_modificacao DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                    )
                ''')
                
                # Tabela de Logs
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS logs_acesso (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        usuario_id INTEGER NOT NULL,
                        data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
                        acao TEXT NOT NULL,
                        ip TEXT,
                        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                    )
                ''')
                
                # Tabela de Configurações
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS configuracoes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        usuario_id INTEGER NOT NULL,
                        tempo_sessao INTEGER DEFAULT 900,
                        tempo_expiracao_senha INTEGER DEFAULT 432000,
                        tema TEXT DEFAULT 'dark',
                        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                    )
                ''')
                
                # Tabela de Histórico de Senhas
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS historico_senhas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        senha_id INTEGER NOT NULL,
                        senha_antiga TEXT NOT NULL,
                        data_modificacao DATETIME DEFAULT CURRENT_TIMESTAMP,
                        modificado_por INTEGER NOT NULL,
                        FOREIGN KEY (senha_id) REFERENCES senhas(id),
                        FOREIGN KEY (modificado_por) REFERENCES usuarios(id)
                    )
                ''')
                
                conn.commit()
                self.logger.info("Tabelas criadas/verificadas com sucesso")
                
        except Exception as e:
            self.logger.error(f"Erro ao criar tabelas: {str(e)}")
            raise