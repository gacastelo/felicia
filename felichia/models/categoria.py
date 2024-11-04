from utils.database import Database

class Categoria:
    def __init__(self, nome, descricao=None, cor=None):
        self.nome = nome
        self.descricao = descricao
        self.cor = cor
        self.db = Database()
    
    def salvar(self):
        with self.db.conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO categorias (nome, descricao, cor)
                VALUES (?, ?, ?)
            ''', (self.nome, self.descricao, self.cor))
            return True
    
    @classmethod
    def listar_todas(cls):
        with Database().conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT nome, descricao, cor FROM categorias')
            return cursor.fetchall()
