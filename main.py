from datetime import datetime, timedelta
from package.usuarios import Usuario
from package.atividades.tarefa import Tarefa
from package.atividades.habitos import Habito
from package.Agente import AgenteUniversitario
from package.Agente_conhecimento import BaseDeConhecimento
import os


def main():
    caminho = "data/save.json"
    if os.path.exists(caminho):
        carregar = input("Deseja carregar seus dados salvos? (s/n): ").lower()
        if carregar == "s":
            user = Usuario.carregar_json(caminho)
            print(f"Bem-vindo de volta, {user.nome}!")
        else:
            nome_usuario = input("Digite seu nome: ")
            user = Usuario(nome_usuario)
    else:
        nome_usuario = input("Digite seu nome: ")
        user = Usuario(nome_usuario)

    while True:
        print("\n1. Adicionar tarefa\n2. Adicionar hábito\n3. Listar atividades\n4. Salvar e sair")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            titulo = input("Título da tarefa: ")
            dias = int(input("Prazo em quantos dias? "))
            data_entrega = datetime.now() + timedelta(days=dias)
            tarefa = Tarefa(titulo, data_entrega)
            user.adicionar_tarefa(tarefa)
        elif opcao == "2":
            titulo = input("Título do hábito: ")
            frequencia = input("Frequência (ex: diário, semanal): ")
            habito = Habito(titulo, frequencia)
            user.adicionar_habito(habito)
        elif opcao == "3":
            print("\n--- Tarefas ---")
            for t in user.tarefas:
                print(t)
            print("\n--- Hábitos ---")
            for h in user.habitos:
                print(h)
        elif opcao == "4":
            user.salvar_json(caminho)
            print("Dados salvos! Até logo!")
            break
        else:
            print("Opção inválida.")

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

