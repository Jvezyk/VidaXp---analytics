from package.atividades.atividade import Atividade


class Habito(Atividade):
    def __init__(self, titulo, frequencia="diário", status='pendente'):
        super().__init__(titulo, status)
        self.frequencia = frequencia

    def concluir(self):
        self.status = 'concluído'
