from datetime import datetime
from package.atividades.atividade import Atividade

class Tarefa(Atividade):
    def __init__(self, titulo: str, xp: int, data_limite: datetime):
        super().__init__(titulo, xp)
        self.data_limite = data_limite
    
    def concluir(self):
        self.status = 'concluida'
        print(f"Tarefa '{self.titulo}' concluída! Você ganhou {self.xp} XP.")
    
    def __str__(self):
        return f"Tarefa: {super().__str__()} - Prazo: {self.data_limite.strftime('%d/%m/%Y')}"
