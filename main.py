from datetime import datetime, timedelta
from package.usuarios import Usuario
from package.atividades.tarefa import Tarefa
from package.atividades.habitos import Habito
from package.Agente import AgenteUniversitario
from package.Agente_conhecimento import BaseDeConhecimento


def main():
    user = Usuario("João")

    Tarefas = Tarefa("Entregar trabalho de OO", datetime.now() + timedelta(days=7))
    Habitos = Habito("Estudar programação", "diário")

    user.adicionar_tarefa(Tarefas)
    user.adicionar_habito(Habitos)

    print("--- Atividades ---")
    for tarefa in user.tarefas:
        print(tarefa)
    for habito in user.habitos:
        print(habito)

    print("\n--- Concluindo atividades ---")
    user.concluir_tarefa(Tarefas)
    user.concluir_habito(Habitos)


    # base = BaseDeConhecimento("data/base_conhecimento.json")
    # agente = AgenteUniversitario("GAMA.BOT", "UnB Gama", base)

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
