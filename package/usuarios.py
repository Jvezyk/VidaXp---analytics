from package.atividades.tarefa import Tarefa
from package.atividades.habitos import Habito

class Usuario:
    def __init__(self, nome: str):
        self.nome = nome
        self.xp_total = 0
        self.nivel = 1
        self.tarefas = []
        self.habitos = []
    
    def adicionar_tarefa(self, tarefa: Tarefa):
        self.tarefas.append(tarefa)
    
    def adicionar_habito(self, habito: Habito):
        self.habitos.append(habito)
    
    def ganhar_xp(self, xp: int):
        self.xp_total += xp
        self.verificar_nivel()
    
    def verificar_nivel(self):
        nivel_atual = self.xp_total // 100 + 1
        if nivel_atual > self.nivel:
            self.nivel = nivel_atual
            print(f"Parabéns {self.nome}! Você subiu para o nível {self.nivel}!")
    
    def concluir_tarefa(self, tarefa: Tarefa):
        tarefa.concluir()
        self.ganhar_xp(tarefa.xp)
    
    def concluir_habito(self, habito: Habito):
        habito.concluir()
        self.ganhar_xp(habito.xp)
