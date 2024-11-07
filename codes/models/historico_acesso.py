from datetime import datetime
import socket
import requests
import logging
from utils.database import Database

class HistoricoAcesso:
    def __init__(self, usuario_id):
        self.usuario_id = usuario_id
        self.db = Database()
    
    def registrar_acesso(self, acao: str):
        """Registra um acesso com informações detalhadas"""
        try:
            ip_local = socket.gethostbyname(socket.gethostname())
            ip_publico = self._get_ip_publico()
            
            with self.db.conectar() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO logs_acesso (
                        usuario_id, acao, ip, detalhes
                    ) VALUES (?, ?, ?, ?)
                ''', (
                    self.usuario_id,
                    acao,
                    ip_publico or ip_local,
                    self._get_detalhes_sistema()
                ))
                
        except Exception as e:
            logging.error(f"Erro ao registrar acesso: {str(e)}")
    
    def _get_ip_publico(self) -> str:
        """Obtém o IP público do usuário"""
        try:
            response = requests.get('https://api.ipify.org?format=json')
            return response.json()['ip']
        except:
            return None
    
    def _get_detalhes_sistema(self) -> str:
        """Obtém detalhes do sistema"""
        import platform
        return f"OS: {platform.system()} {platform.release()}"
