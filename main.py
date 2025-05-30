from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta


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
    registros = db.relationship(
        'RegistroHabito', backref='habito', cascade="all, delete-orphan")

    def concluir(self):
        self.status = 'concluído'


class RegistroHabito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, default=date.today)
    concluido = db.Column(db.Boolean, default=False)
    habito_id = db.Column(db.Integer, db.ForeignKey(
        'habito.id'), nullable=False)


# Função que renova hábitos diariamente
def renovar_registros_habitos(usuario_id):
    hoje = date.today()
    habitos = Habito.query.filter_by(usuario_id=usuario_id).all()
    for habito in habitos:
        existe = RegistroHabito.query.filter_by(
            habito_id=habito.id, data=hoje).first()
        if not existe:
            novo = RegistroHabito(habito_id=habito.id, data=hoje)
            db.session.add(novo)
    db.session.commit()


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


@app.route("/criar_usuario", methods=["GET", "POST"])
def criar_usuario():
    if request.method == "POST":
        nome = request.form["nome"]
        senha = request.form["senha"]
        if not Usuario.query.filter_by(nome=nome).first():
            usuario = Usuario(nome=nome, senha=senha)
            db.session.add(usuario)
            db.session.commit()
            session["usuario_id"] = usuario.id
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
        nova_senha = request.form.get("senha")
        if nova_senha:
            usuario.senha = nova_senha
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


@app.route("/")
def inicio():
    if not Usuario.query.first():
        return redirect(url_for("criar_usuario"))
    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    usuario_id = session.get("usuario_id")
    if not usuario_id:
        return redirect(url_for("login"))
    renovar_registros_habitos(usuario_id)
    usuario = Usuario.query.get(usuario_id)
    tarefas = usuario.tarefas
    habitos = usuario.habitos
    return render_template("index.html", tarefas=tarefas, habitos=habitos, aba="dashboard")


@app.route("/tarefas")
def tarefas():
    usuario_id = session.get("usuario_id")
    tarefas = Tarefa.query.filter_by(usuario_id=usuario_id).all()
    return render_template("index.html", tarefas=tarefas, aba="tarefas")


@app.route("/habitos")
def habitos():
    usuario_id = session.get("usuario_id")
    habitos = Habito.query.filter_by(usuario_id=usuario_id).all()
    return render_template("index.html", habitos=habitos, aba="habitos")


@app.route("/adicionar_tarefa", methods=["POST"])
def adicionar_tarefa():
    usuario_id = session.get("usuario_id")
    usuario = Usuario.query.get(usuario_id)
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
    hoje = date.today()
    registro = RegistroHabito.query.filter_by(
        habito_id=habito.id, data=hoje).first()
    if registro:
        registro.concluido = True
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
    usuario_id = session.get("usuario_id")
    hoje = date.today()

    tarefas_concluidas = Tarefa.query.filter_by(
        usuario_id=usuario_id, status='concluída').count()
    tarefas_pendentes = Tarefa.query.filter_by(
        usuario_id=usuario_id, status='pendente').count()

    registros = RegistroHabito.query.join(Habito).filter(
        Habito.usuario_id == usuario_id,
        RegistroHabito.data == hoje
    ).all()

    habitos_concluidos = sum(1 for r in registros if r.concluido)
    habitos_total = len(registros)

    return jsonify({
        "tarefas_concluidas": tarefas_concluidas,
        "tarefas_pendentes": tarefas_pendentes,
        "habitos_concluidos": habitos_concluidos,
        "habitos_total": habitos_total
    })


@app.route("/dados_grafico_progresso")
def dados_grafico_progresso():
    usuario_id = session.get("usuario_id")
    # Descobre o menor e maior dia de conclusão
    primeira_tarefa = Tarefa.query.filter_by(
        usuario_id=usuario_id).order_by(Tarefa.data_entrega).first()
    hoje = date.today()
    if primeira_tarefa and primeira_tarefa.data_entrega:
        inicio_dt = primeira_tarefa.data_entrega
        if isinstance(inicio_dt, datetime):
            inicio_dt = inicio_dt.date()
    else:
        inicio_dt = hoje
    fim_dt = hoje

    dias = []
    tarefas = []
    habitos = []

    for n in range((fim_dt - inicio_dt).days + 1):
        dia = inicio_dt + timedelta(days=n)
        dias.append(dia.strftime("%Y-%m-%d"))
        tarefas_concluidas = Tarefa.query.filter_by(
            usuario_id=usuario_id, status='concluída'
        ).filter(db.func.date(Tarefa.data_entrega) == dia).count()
        tarefas.append(tarefas_concluidas)

        registros = RegistroHabito.query.join(Habito).filter(
            Habito.usuario_id == usuario_id,
            RegistroHabito.data == dia,
            RegistroHabito.concluido == True
        ).count()
        habitos.append(registros)

    return jsonify({"dias": dias, "tarefas": tarefas, "habitos": habitos})


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
