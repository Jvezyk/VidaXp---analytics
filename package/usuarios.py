import json
from package.atividades.tarefa import Tarefa
from package.atividades.habitos import Habito
from datetime import datetime, timedelta


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

    def salvar_json(self, caminho):
        dados = {
            "Nome": self.nome,
            "tarefas": [
                {
                    "titulo": t.titulo,
                    "status": t.status,
                    "data_criacao": t.data_crição.isoformat(),
                    "data_entrega": t.data_entrega.isoformat()
                } for t in self.tarefas
            ],
            "habitos": [
                {
                    "titulo": h.titulo,
                    "status": h.status,
                    "data_criacao": h.data_criacao.isoformat(),
                    "data_entrega": h.data_entrega.isoformat()
                } for h in self.habitos
            ]
        }
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

    @classmethod
    def carregar_json(cls, caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
        usuario = cls(dados["nome"])
        for t in dados["tarefas"]:
            tarefa = Tarefa(
                t["titulo"],
                datetime.fromisoformat(t["data_entrega"])
            )
            tarefa.status = t["status"]
            tarefa.data_criacao = datetime.fromisoformat(t["data_criacao"])
            usuario.adicionar_tarefa(tarefa)
        for h in dados["habitos"]:
            habito = Habito(
                h["titulo"],
                h["frequencia"]
            )
            habito.status = h["status"]
            habito.data_criacao = datetime.fromisoformat(h["data_criacao"])
            usuario.adicionar_habito(habito)
        return usuario
