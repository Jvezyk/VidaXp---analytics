from abc import ABC, abstractmethod
from datetime import datetime

class Atividade(ABC):
    def __init__(self, titulo: str, xp: int):
        self.titulo = titulo
        self.xp = xp
        self.status = 'pendente'  # ou 'concluida'
        self.data_criacao = datetime.now()
    
    @abstractmethod
    def concluir(self):
        pass
    
    def __str__(self):
        return f"{self.titulo} [{self.status}] - XP: {self.xp}"
