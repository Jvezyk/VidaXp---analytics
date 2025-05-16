from datetime import datetime
from package.atividades.atividade import Atividade


class Tarefa(Atividade):
    def __init__(self, titulo:str, data_limite: datetime):
        super().__init__(titulo)
        self.data_limite = data_limite

    def concluir(self):
        self.status = 'concluida'
        print(f"Tarefa '{self.titulo}' concluída!")

    def __str__(self):
        return f"Tarefa: {super().__str__()} - Prazo: {self.data_limite.strftime('%d/%m/%Y')}"
