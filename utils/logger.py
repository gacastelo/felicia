import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def configurar_logging():
    # Criar diretório de logs se não existir
    Path("logs").mkdir(exist_ok=True)
    
    logger = logging.getLogger('gerenciador_senhas')
    logger.setLevel(logging.INFO)
    
    handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=1024*1024,  # 1MB
        backupCount=5
    )
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)