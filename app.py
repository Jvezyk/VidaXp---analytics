from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vidaxp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelos do banco


class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), default='pendente')
    data_entrega = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def concluir(self):
        self.status = 'concluída'


class Habito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), default='pendente')
    frequencia = db.Column(db.String(20), default='diário')

    def concluir(self):
        self.status = 'concluído'

# Rotas


@app.route("/")
def dashboard():
    tarefas = Tarefa.query.all()
    habitos = Habito.query.all()
    return render_template("index.html", tarefas=tarefas, habitos=habitos, aba="dashboard")


@app.route("/tarefas")
def tarefas():
    tarefas = Tarefa.query.all()
    return render_template("index.html", tarefas=tarefas, aba="tarefas")


@app.route("/habitos")
def habitos():
    habitos = Habito.query.all()
    return render_template("index.html", habitos=habitos, aba="habitos")


@app.route("/adicionar_tarefa", methods=["POST"])
def adicionar_tarefa():
    titulo = request.form["titulo"]
    tarefa = Tarefa(titulo=titulo)
    db.session.add(tarefa)
    db.session.commit()
    return redirect(url_for("tarefas"))


@app.route("/concluir_tarefa/<int:id>")
def concluir_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    tarefa.concluir()
    db.session.commit()
    return redirect(url_for("tarefas"))


@app.route("/remover_tarefa/<int:id>")
def remover_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    db.session.delete(tarefa)
    db.session.commit()
    return redirect(url_for("tarefas"))


@app.route("/adicionar_habito", methods=["POST"])
def adicionar_habito():
    titulo = request.form["titulo"]
    habito = Habito(titulo=titulo)
    db.session.add(habito)
    db.session.commit()
    return redirect(url_for("habitos"))


@app.route("/concluir_habito/<int:id>")
def concluir_habito(id):
    habito = Habito.query.get_or_404(id)
    habito.concluir()
    db.session.commit()
    return redirect(url_for("habitos"))


@app.route("/remover_habito/<int:id>")
def remover_habito(id):
    habito = Habito.query.get_or_404(id)
    db.session.delete(habito)
    db.session.commit()
    return redirect(url_for("habitos"))


@app.route("/dados_grafico")
def dados_grafico():
    tarefas_concluidas = Tarefa.query.filter_by(status='concluída').count()
    habitos_concluidos = Habito.query.filter_by(status='concluído').count()
    return jsonify({"tarefas": tarefas_concluidas, "habitos": habitos_concluidos})


# Crie o banco de dados na primeira execução
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
