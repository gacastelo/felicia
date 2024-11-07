import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path

def configurar_logging():
    # Criar diretório de logs se não existir
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configurar o logger
    logger = logging.getLogger('gerenciador_senhas')
    logger.setLevel(logging.INFO)
    
    # Criar handler para arquivo
    handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=1024*1024,  # 1MB
        backupCount=5,
        encoding='utf-8'
    )
    
    # Definir formato do log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Adicionar handler ao logger
    logger.addHandler(handler)
    
    # Adicionar handler para console também
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

# Criar logger global
logger = configurar_logging()
