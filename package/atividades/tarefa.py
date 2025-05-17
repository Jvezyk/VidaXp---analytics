from datetime import datetime
from package.atividades.atividade import Atividade


class Tarefa(Atividade):
    def __init__(self, titulo: str, data_entrega: datetime):
        super().__init__(titulo)
        self.data_entrega = data_entrega

    def concluir(self):
        print(f"Tarefa: '{self.titulo}' concluída!")

    def __str__(self):
        return f"Tarefa: {super().__str__()} - Prazo: {self.data_entrega.strftime('%d/%m/%Y')}"

