from package.Agente_conhecimento import BaseDeConhecimento


class AgenteUniversitario:
    def __init__(self, nome, universidade, Agente_conhecimento):
        self.nome = nome
        self.universidade = universidade
        self.base = Agente_conhecimento

    def responder(self, pergunta):
        return self.base.buscar_resposta(pergunta)
