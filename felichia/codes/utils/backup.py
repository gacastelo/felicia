import sqlite3
import zipfile
import json
from datetime import datetime
from pathlib import Path
import shutil
import logging
from utils.database import Database
from tkinter import filedialog
import os

class BackupService:
    def __init__(self):
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
        self.db_path = Path("data/senhas.db")
        self.setup_logging()
    
    def setup_logging(self):
        """Configura o sistema de logging"""
        self.logger = logging.getLogger('backup_service')
        self.logger.setLevel(logging.INFO)
        
        # Cria handler para arquivo
        log_file = Path("logs/backup.log")
        log_file.parent.mkdir(exist_ok=True)
        
        handler = logging.FileHandler(log_file)
        handler.setLevel(logging.INFO)
        
        # Formato do log
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        self.logger.addHandler(handler)
    
    def criar_backup(self, usuario_id=None):
        """Cria um backup do banco de dados"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / f"backup_{timestamp}"
            backup_path.mkdir(exist_ok=True)
            
            # Copia o arquivo do banco de dados
            backup_db = backup_path / "senhas.db"
            
            with sqlite3.connect(self.db_path) as src, \
                 sqlite3.connect(backup_db) as dst:
                src.backup(dst)
            
            # Exporta os dados em JSON (opcional)
            self._exportar_json(backup_path, usuario_id)
            
            # Compacta o backup
            zip_path = self.backup_dir / f"backup_{timestamp}.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in backup_path.rglob('*'):
                    zipf.write(file, file.relative_to(backup_path))
            
            # Remove diretório temporário
            shutil.rmtree(backup_path)
            
            self.logger.info(f"Backup criado com sucesso: {zip_path}")
            self._manter_apenas_ultimos_backups()
            
            return True, f"Backup criado com sucesso: {zip_path}"
        
        except Exception as e:
            self.logger.error(f"Erro ao criar backup: {str(e)}")
            return False, f"Erro ao criar backup: {str(e)}"
    
    def restaurar_backup(self, backup_path):
        """Restaura um backup"""
        try:
            # Extrai o backup
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                temp_dir = self.backup_dir / "temp_restore"
                temp_dir.mkdir(exist_ok=True)
                zipf.extractall(temp_dir)
            
            # Restaura o banco de dados
            backup_db = temp_dir / "senhas.db"
            
            # Faz backup do banco atual antes de restaurar
            self.criar_backup()
            
            # Restaura o banco
            with sqlite3.connect(backup_db) as src, \
                 sqlite3.connect(self.db_path) as dst:
                src.backup(dst)
            
            # Remove diretório temporário
            shutil.rmtree(temp_dir)
            
            self.logger.info(f"Backup restaurado com sucesso: {backup_path}")
            return True, "Backup restaurado com sucesso"
        
        except Exception as e:
            self.logger.error(f"Erro ao restaurar backup: {str(e)}")
            return False, f"Erro ao restaurar backup: {str(e)}"
    
    def _exportar_json(self, backup_path, usuario_id=None):
        """Exporta os dados em formato JSON"""
        db = Database()
        with db.conectar() as conn:
            cursor = conn.cursor()
            
            # Consulta para usuários
            if usuario_id:
                cursor.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,))
            else:
                cursor.execute("SELECT * FROM usuarios")
            usuarios = cursor.fetchall()
            
            # Consulta para senhas
            if usuario_id:
                cursor.execute("SELECT * FROM senhas WHERE usuario_id = ?", (usuario_id,))
            else:
                cursor.execute("SELECT * FROM senhas")
            senhas = cursor.fetchall()
            
            # Cria dicionário com os dados
            dados = {
                "usuarios": usuarios,
                "senhas": senhas
            }
            
            # Salva em arquivo JSON
            json_path = backup_path / "dados.json"
            with open(json_path, 'w') as f:
                json.dump(dados, f, indent=4, default=str)
    
    def _manter_apenas_ultimos_backups(self, max_backups=5):
        """Mantém apenas os últimos N backups"""
        backups = sorted(
            self.backup_dir.glob("*.zip"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        for backup in backups[max_backups:]:
            backup.unlink()
            self.logger.info(f"Backup antigo removido: {backup}")
    
    def listar_backups(self):
        """Lista todos os backups disponíveis"""
        return sorted(
            self.backup_dir.glob("*.zip"),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
    
    def exportar_backup(self, usuario_id):
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json")],
                initialfile=f"backup_senhas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            
            if not filename:
                return False, "Operação cancelada"
            
            db = Database()
            with db.conectar() as conn:
                cursor = conn.cursor()
                
                # Busca dados do usuário - removido o campo 'nome' que não existe
                cursor.execute("""
                    SELECT id, username
                    FROM usuarios 
                    WHERE id = ?
                """, (usuario_id,))
                usuario = cursor.fetchone()
                
                if not usuario:
                    return False, "Usuário não encontrado"
                
                # Busca senhas do usuário
                cursor.execute("""
                    SELECT id, usuario_id, site, username, senha_criptografada,
                           data_criacao, data_modificacao
                    FROM senhas 
                    WHERE usuario_id = ?
                """, (usuario_id,))
                senhas = cursor.fetchall()
                
                # Prepara dados para exportação - ajustado para usar apenas username
                dados_backup = {
                    "usuario": {
                        "id": usuario[0],
                        "username": usuario[1]
                    },
                    "senhas": []
                }
                
                # Adiciona as senhas ao backup
                for senha in senhas:
                    dados_backup["senhas"].append({
                        "id": senha[0],
                        "usuario_id": senha[1],
                        "site": senha[2],
                        "username": senha[3],
                        "senha_criptografada": senha[4],
                        "data_criacao": str(senha[5]),
                        "data_modificacao": str(senha[6])
                    })
                
                # Salva o arquivo JSON
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(dados_backup, f, indent=4, ensure_ascii=False, default=str)
                
                self.logger.info(f"Backup exportado com sucesso para: {filename}")
                return True, "Backup exportado com sucesso!"
                
        except Exception as e:
            self.logger.error(f"Erro ao exportar backup: {str(e)}")
            return False, f"Erro ao exportar backup: {str(e)}"
    
    def importar_backup(self, usuario_id):
        try:
            # Abre diálogo para selecionar arquivo
            filename = filedialog.askopenfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json")]
            )
            
            if not filename:  # Se usuário cancelou
                return False, "Operação cancelada"
            
            # Lê o arquivo JSON
            with open(filename, 'r', encoding='utf-8') as f:
                dados_backup = json.load(f)
            
            # Verifica se o backup pertence ao usuário correto
            if dados_backup["usuario"]["id"] != usuario_id:
                return False, "Este backup pertence a outro usuário"
            
            # Importa as senhas
            db = Database()
            with db.conectar() as conn:
                cursor = conn.cursor()
                
                for senha in dados_backup["senhas"]:
                    # Verifica se a senha já existe
                    cursor.execute(
                        "SELECT id FROM senhas WHERE id = ? AND usuario_id = ?",
                        (senha["id"], usuario_id)
                    )
                    
                    if cursor.fetchone():
                        # Atualiza senha existente
                        cursor.execute("""
                            UPDATE senhas 
                            SET site = ?, username = ?, senha_criptografada = ?,
                                data_modificacao = CURRENT_TIMESTAMP
                            WHERE id = ? AND usuario_id = ?
                        """, (
                            senha["site"], senha["username"],
                            senha["senha_criptografada"],
                            senha["id"], usuario_id
                        ))
                    else:
                        # Insere nova senha
                        cursor.execute("""
                            INSERT INTO senhas (site, usuario_id, username,
                                              senha_criptografada)
                            VALUES (?, ?, ?, ?)
                        """, (
                            senha["site"], usuario_id, senha["username"],
                            senha["senha_criptografada"]
                        ))
                
                conn.commit()
            
            return True, "Backup importado com sucesso!"
            
        except Exception as e:
            self.logger.error(f"Erro ao importar backup: {str(e)}")
            return False, f"Erro ao importar backup: {str(e)}"