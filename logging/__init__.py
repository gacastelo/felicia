import logging
import os
import sys
from pathlib import Path

def setup_logging():
    try:
        # Define o diretório de logs baseado no ambiente
        if getattr(sys, 'frozen', False):
            # Se for executável, usa AppData
            base_dir = os.path.join(os.environ.get('APPDATA', ''), 'Felichia')
        else:
            # Se for desenvolvimento, usa pasta local
            base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Cria pasta logs dentro do diretório base
        log_dir = os.path.join(base_dir, 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        # Caminho completo do arquivo de log
        log_file = os.path.join(log_dir, 'felichia.log')
        
        # Configura o handler de arquivo
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        
        # Configura o logger root
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
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