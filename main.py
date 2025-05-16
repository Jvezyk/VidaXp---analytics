from datetime import datetime, timedelta
from package.usuarios import Usuario
from package.atividades.tarefa import Tarefa
from package.atividades.habitos import Habito
from package.Agente import AgenteUniversitario
from package.Agente_conhecimento import BaseDeConhecimento


def main():
    user = Usuario("João")

    t1 = Tarefa("Entregar trabalho de OO", datetime.now() + timedelta(days=7))
    h1 = Habito("Estudar programação", "diário")

    user.adicionar_tarefa(t1)
    user.adicionar_habito(h1)

    print("--- Atividades ---")
    for t in user.tarefas:
        print(t)
    for h in user.habitos:
        print(h)

    print("\n--- Concluindo atividades ---")
    user.concluir_tarefa(t1)
    user.concluir_habito(h1)

    base = BaseDeConhecimento("data/base_conhecimento.json")
    agente = AgenteUniversitario("GAMA.BOT", "UnB Gama", base)

    # print(
    # f"Olá! Eu sou {agente.nome}, seu assistente da {agente.universidade} 😊")
    # print("Digite uma pergunta ou 'sair' para encerrar.")

    # while True:
    #     pergunta = input("\nVocê: ")
    #     if pergunta.lower() in ["sair", "exit", "quit"]:
    #         print("Agente: Até logo! Bons estudos!")
    #         break
    #     resposta = agente.responder(pergunta)
    #     print(f"Agente: {resposta}")


if __name__ == "__main__":
    main()
