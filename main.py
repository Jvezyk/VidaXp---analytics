from datetime import datetime, timedelta
from package.usuarios import Usuario
from package.atividades.tarefa import Tarefa
from package.atividades.habitos import Habito

def main():
    user = Usuario("João")
    
    t1 = Tarefa("Entregar trabalho de OO", 50, datetime.now() + timedelta(days=3))
    h1 = Habito("Estudar programação", 10, "diário")
    
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
    
    print(f"\nXP total: {user.xp_total} | Nível: {user.nivel}")

if __name__ == "__main__":
    main()
