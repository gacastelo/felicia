from pathlib import Path
import sqlite3
import zipfile
from datetime import datetime
import shutil
import logging
import json

logger = logging.getLogger('gerenciador_senhas')

class BackupService:
    def __init__(self):
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
        self.max_backups = 5  # Manter apenas os 5 backups mais recentes
    
    def criar_backup(self):
        """Cria um backup completo do banco de dados"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"backup_{timestamp}.db"
            
            # Backup do banco de dados
            with sqlite3.connect("database/senhas.db") as src, \
                 sqlite3.connect(backup_file) as dst:
                src.backup(dst)
            
            # Compactar backup
            zip_path = f"{backup_file}.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.write(backup_file, arcname=backup_file.name)
            
            # Remover arquivo .db temporário
            backup_file.unlink()
            
            # Limpar backups antigos
            self.limpar_backups_antigos()
            
            logger.info(f"Backup criado com sucesso: {zip_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao criar backup: {str(e)}")
            return False
    
    def limpar_backups_antigos(self):
        """Mantém apenas os backups mais recentes"""
        backups = sorted(self.backup_dir.glob("*.zip"))
        while len(backups) > self.max_backups:
            backups[0].unlink()  # Remove o backup mais antigo
            backups = backups[1:]
    
    def restaurar_backup(self, backup_path):
        """Restaura um backup específico"""
        try:
            # Extrair backup
            with zipfile.ZipFile(backup_path, 'r') as zip_file:
                zip_file.extractall(self.backup_dir)
            
            db_file = backup_path.replace('.zip', '')
            
            # Criar backup do banco atual antes de restaurar
            shutil.copy2("database/senhas.db", "database/senhas.db.bak")
            
            # Restaurar banco
            with sqlite3.connect(db_file) as src, \
                 sqlite3.connect("database/senhas.db") as dst:
                src.backup(dst)
            
            # Limpar arquivos temporários
            Path(db_file).unlink()
            
            logger.info(f"Backup restaurado com sucesso: {backup_path}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao restaurar backup: {str(e)}")
            return False
