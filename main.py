from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import session, redirect, url_for, render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vidaxp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "um_valor_bem_secreto_e_unico" 
db = SQLAlchemy(app)

# Modelos do banco


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    senha = db.Column(db.String(120), nullable=False)
    tarefas = db.relationship(
        'Tarefa', backref='usuario', cascade="all, delete-orphan")
    habitos = db.relationship(
        'Habito', backref='usuario', cascade="all, delete-orphan")


class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), default='pendente')
    data_entrega = db.Column(db.DateTime, nullable=False, default=datetime.now)
    usuario_id = db.Column(db.Integer, db.ForeignKey(
        'usuario.id'), nullable=False)

    def concluir(self):
        self.status = 'concluída'


class Habito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), default='pendente')
    frequencia = db.Column(db.String(20), default='diário')
    usuario_id = db.Column(db.Integer, db.ForeignKey(
        'usuario.id'), nullable=False)

    def concluir(self):
        self.status = 'concluído'

# Rotas


@app.route("/login", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        nome = request.form["nome"]
        senha = request.form["senha"]
        usuario = Usuario.query.filter_by(nome=nome, senha=senha).first()
        if usuario:
            session["usuario_id"] = usuario.id
            return redirect(url_for("dashboard"))
        else:
            erro = "Usuário ou senha inválidos!"
    return render_template("login.html", erro=erro)


@app.route("/logout")
def logout():
    session.pop("usuario_id", None)
    return redirect(url_for("login"))


@app.route("/")
def inicio():
    if not Usuario.query.first():
        return redirect(url_for("criar_usuario"))
    return redirect(url_for("login"))


@app.route("/criar_usuario", methods=["GET", "POST"])
def criar_usuario():
    if request.method == "POST":
        nome = request.form["nome"]
        senha = request.form["senha"]
        if not Usuario.query.filter_by(nome=nome).first():
            usuario = Usuario(nome=nome, senha=senha)
            db.session.add(usuario)
            db.session.commit()
            session["usuario_id"] = usuario.id  # já faz login automático
            return redirect(url_for("dashboard"))
        else:
            erro = "Usuário já existe!"
            return render_template("criar_usuario.html", erro=erro)
    return render_template("criar_usuario.html")


@app.route("/editar_usuario/<int:id>", methods=["GET", "POST"])
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    if request.method == "POST":
        usuario.nome = request.form["nome"]
        db.session.commit()
        return redirect(url_for("dashboard"))
    return render_template("editar_usuario.html", usuario=usuario)


@app.route("/excluir_usuario/<int:id>", methods=["POST"])
def excluir_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    session.pop("usuario_id", None)
    return redirect(url_for("login"))


@app.route("/inicio")
def dashboard():
    usuario_id = session.get("usuario_id")
    if not usuario_id:
        return redirect(url_for("login"))
    usuario = Usuario.query.get(usuario_id)
    if not usuario:
        return redirect(url_for("criar_usuario"))
    tarefas = usuario.tarefas
    habitos = usuario.habitos
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
    usuario_id = session.get("usuario_id")
    usuario = Usuario.query.get(usuario_id)
    usuario = Usuario.query.first()
    titulo = request.form["titulo"]
    tarefa = Tarefa(titulo=titulo, usuario=usuario)
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
    usuario_id = session.get("usuario_id")
    usuario = Usuario.query.get(usuario_id)
    titulo = request.form["titulo"]
    habito = Habito(titulo=titulo, usuario=usuario)
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
