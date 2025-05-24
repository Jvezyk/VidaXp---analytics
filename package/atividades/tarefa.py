from datetime import datetime
from package.atividades.atividade import Atividade


class Tarefa(Atividade):
    def __init__(self, titulo, data_entrega=None, status='pendente'):
        super().__init__(titulo, status)
        self.data_entrega = data_entrega or datetime.now()

    def concluir(self):
        self.status = 'concluída'

