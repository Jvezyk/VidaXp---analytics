import json
from package.atividades.tarefa import Tarefa
from package.atividades.habitos import Habito
from datetime import datetime, timedelta


class Usuario:
    def __init__(self, nome):
        self.nome = nome
        self.tarefas = []
        self.habitos = []

    def adicionar_tarefa(self, tarefa):
        self.tarefas.append(tarefa)

    def adicionar_habito(self, habito):
        self.habitos.append(habito)

    def tarefas_pendentes(self):
        return [t for t in self.tarefas if t.is_pendente()]

    def tarefas_concluidas(self):
        return [t for t in self.tarefas if t.is_concluida()]

    def habitos_pendentes(self):
        return [h for h in self.habitos if h.is_pendente()]

    def habitos_concluidos(self):
        return [h for h in self.habitos if h.is_concluido()]