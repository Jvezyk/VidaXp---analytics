import json


class BaseDeConhecimento:
    def __init__(self, caminho_arquivo):
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            self.base = json.load(f)

    def buscar_resposta(self, pergunta_usuario):
        pergunta_usuario = pergunta_usuario.strip().lower()

        for chave, resposta in self.base.items():
            if chave in pergunta_usuario:
                return resposta

        return "Desculpe, não sei responder isso ainda. Tente outra pergunta"
