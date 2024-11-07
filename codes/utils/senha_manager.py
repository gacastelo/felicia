import string
import secrets
from typing import Dict

class SenhaManager:
    def __init__(self):
        self.min_comprimento = 8
        self.caracteres = {
            'maiusculas': string.ascii_uppercase,
            'minusculas': string.ascii_lowercase,
            'numeros': string.digits,
            'especiais': string.punctuation
        }
    
    def gerar_senha_forte(self, tamanho: int = 16) -> str:
        """Gera uma senha forte aleatória"""
        if tamanho < self.min_comprimento:
            tamanho = self.min_comprimento
            
        # Garantir pelo menos um caractere de cada tipo
        senha = [
            secrets.choice(self.caracteres['maiusculas']),
            secrets.choice(self.caracteres['minusculas']),
            secrets.choice(self.caracteres['numeros']),
            secrets.choice(self.caracteres['especiais'])
        ]
        
        # Completar o resto da senha
        caracteres_todos = ''.join(self.caracteres.values())
        for _ in range(tamanho - len(senha)):
            senha.append(secrets.choice(caracteres_todos))
            
        # Embaralhar a senha
        secrets.SystemRandom().shuffle(senha)
        return ''.join(senha)
    
    def verificar_forca_senha(self, senha: str) -> Dict[str, bool]:
        """Verifica a força da senha e retorna um dicionário com os critérios"""
        return {
            'comprimento': len(senha) >= self.min_comprimento,
            'maiusculas': any(c in self.caracteres['maiusculas'] for c in senha),
            'minusculas': any(c in self.caracteres['minusculas'] for c in senha),
            'numeros': any(c in self.caracteres['numeros'] for c in senha),
            'especiais': any(c in self.caracteres['especiais'] for c in senha)
        }
    
    def calcular_pontuacao_senha(self, senha: str) -> int:
        """Calcula uma pontuação de 0 a 100 para a senha"""
        criterios = self.verificar_forca_senha(senha)
        pontuacao = sum(criterios.values()) * 20  # 20 pontos por critério
        
        # Bônus por comprimento extra
        if len(senha) > self.min_comprimento:
            pontuacao += min((len(senha) - self.min_comprimento) * 2, 20)
            
        return min(pontuacao, 100)
