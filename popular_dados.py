from main import db, app, Usuario, Tarefa, Habito, RegistroHabito, HistoricoAtividade
from datetime import date, timedelta

## Caso queira testar sem esperar dias para ver o gráfico.

def popular_dados_teste(usuario_id):
    hoje = date.today()
    # Limpa tarefas e histórico antigos
    Tarefa.query.filter_by(usuario_id=usuario_id).delete()
    HistoricoAtividade.query.filter_by(usuario_id=usuario_id).delete()
    db.session.commit()

    # Cria 7 tarefas, uma para cada dia da semana passada até hoje
    for i in range(7):
        dia = hoje - timedelta(days=6-i)
        tarefa = Tarefa(
            titulo=f"Tarefa {i+1}",
            prazo=dia,
            data_entrega=dia,
            usuario_id=usuario_id,
            status='pendente'
        )
        db.session.add(tarefa)
        db.session.commit()

        # Só conclui algumas tarefas (ex: conclui as de índice par)
        if i % 2 == 0:
            tarefa.status = 'concluída'
            db.session.commit()
            historico = HistoricoAtividade(
                usuario_id=usuario_id,
                tipo='tarefa',
                data=dia,
                titulo=tarefa.titulo
            )
            db.session.add(historico)
            db.session.commit()
    print("Dados de teste populados!")

if __name__ == "__main__":
    with app.app_context():
        usuarios = Usuario.query.all()
        for usuario in usuarios:
            popular_dados_teste(usuario.id)