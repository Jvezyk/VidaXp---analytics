from package.atividades.tarefa import Tarefa
from package.atividades.habitos import Habito


class Usuario:
    def __init__(self, nome: str):
        self.nome = nome
        self.tarefas = []
        self.habitos = []

    def adicionar_tarefa(self, tarefa: Tarefa):
        self.tarefas.append(tarefa)

    def adicionar_habito(self, habito: Habito):
        self.habitos.append(habito)

    def concluir_tarefa(self, tarefa: Tarefa):
        tarefa.concluir()

    def concluir_habito(self, habito: Habito):
        habito.concluir()
