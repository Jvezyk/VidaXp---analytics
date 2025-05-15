from package.atividades.atividade import Atividade

class Habito(Atividade):
    def __init__(self, titulo: str, xp: int, frequencia: str):
        super().__init__(titulo, xp)
        self.frequencia = frequencia  # ex: 'diário', 'semanal'
    
    def concluir(self):
        # Para hábito, não fecha status, pode registrar múltiplas vezes
        print(f"Hábito '{self.titulo}' marcado como cumprido! Você ganhou {self.xp} XP.")
    
    def __str__(self):
        return f"Hábito: {super().__str__()} - Frequência: {self.frequencia}"
