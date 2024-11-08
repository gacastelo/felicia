import logging
import os
import sys
from datetime import datetime

def setup_logging():
    # Configure o logging básico primeiro
    logging.basicConfig(level=logging.INFO)
    
    # Depois configure os handlers específicos
    try:
        log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f'app_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        
        # Configura o logger root
        root_logger = logging.getLogger()
        root_logger.addHandler(file_handler)
        
        # Adiciona também um handler para console em desenvolvimento
        if not getattr(sys, 'frozen', False):
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(
                logging.Formatter('%(levelname)s: %(message)s')
            )
            root_logger.addHandler(console_handler)
        
        logging.info('Sistema de logging iniciado com sucesso')
        
    except Exception as e:
        # Em caso de erro, tenta criar um arquivo de log de erro no desktop
        try:
            desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
            with open(os.path.join(desktop, 'felichia_error.log'), 'w') as f:
                f.write(f'Erro ao configurar logging: {str(e)}')
        except:
            pass  # Se nem isso funcionar, silenciosamente falha
        
        # Configura logging apenas para console
        logging.basicConfig(
            level=logging.INFO,
            format='%(levelname)s: %(message)s'
        )

# Inicializa o logging
setup_logging() 