from abc import ABC, abstractmethod

class Atividade(ABC):
    def __init__(self, titulo, status='pendente'):
        self.titulo = titulo
        self.status = status

    @abstractmethod
    def concluir(self):
        pass

    def is_pendente(self):
        return self.status == 'pendente'

    def is_concluida(self):
        return self.status in ['concluída', 'concluído']