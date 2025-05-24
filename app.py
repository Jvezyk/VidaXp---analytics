from flask import Flask, render_template, request, redirect, url_for
from package.usuarios import Usuario
from package.atividades.tarefa import Tarefa
from package.atividades.habitos import Habito
from datetime import datetime

app = Flask(__name__)
usuario = Usuario("Aluno")


@app.route("/")
def index():
    return render_template("index.html", usuario=usuario)


@app.route("/adicionar_tarefa", methods=["POST"])
def adicionar_tarefa():
    titulo = request.form["titulo"]
    tarefa = Tarefa(titulo, data_entrega=datetime.now())
    usuario.adicionar_tarefa(tarefa)
    return redirect(url_for("index"))


@app.route("/concluir_tarefa/<int:index>")
def concluir_tarefa(index):
    tarefa = usuario.tarefas[index]
    tarefa.concluir()
    return redirect(url_for("index"))


@app.route("/adicionar_habito", methods=["POST"])
def adicionar_habito():
    titulo = request.form["titulo"]
    habito = Habito(titulo, frequencia="diário")
    usuario.adicionar_habito(habito)
    return redirect(url_for("index"))


@app.route("/concluir_habito/<int:index>")
def concluir_habito(index):
    habito = usuario.habitos[index]
    habito.concluir()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
