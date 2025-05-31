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
    prazo = db.Column(db.Date)
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


class HistoricoAtividade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    tipo = db.Column(db.String(20))  # 'tarefa' ou 'habito'
    data = db.Column(db.Date)
    titulo = db.Column(db.String(120))


class HistoricoPendencias(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    data = db.Column(db.Date)
    tarefas_pendentes = db.Column(db.Integer)
    habitos_pendentes = db.Column(db.Integer)
    habitos_concluidos = db.Column(db.Integer)


def registrar_snapshot_pendencias(usuario_id, dia):
    tarefas_pendentes = Tarefa.query.filter(
        Tarefa.usuario_id == usuario_id,
        Tarefa.status == 'pendente',
        Tarefa.prazo.isnot(None),
        Tarefa.prazo <= dia
    ).count()
    registros_total = RegistroHabito.query.join(Habito).filter(
        Habito.usuario_id == usuario_id,
        RegistroHabito.data == dia
    ).count()
    registros_concluidos = RegistroHabito.query.join(Habito).filter(
        Habito.usuario_id == usuario_id,
        RegistroHabito.data == dia,
        RegistroHabito.concluido == True
    ).count()
    habitos_pendentes = registros_total - registros_concluidos

    snap = HistoricoPendencias(
        usuario_id=usuario_id,
        data=dia,
        tarefas_pendentes=tarefas_pendentes,
        habitos_pendentes=habitos_pendentes,
        habitos_concluidos=registros_concluidos
    )
    db.session.add(snap)
    db.session.commit()


class RegistroHabito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, default=date.today)
    concluido = db.Column(db.Boolean, default=False)
    habito_id = db.Column(db.Integer, db.ForeignKey(
        'habito.id'), nullable=False)


def renovar_registros_habitos(usuario_id):
    hoje = date.today()
    habitos = Habito.query.filter_by(usuario_id=usuario_id).all()
    for habito in habitos:
        existe = RegistroHabito.query.filter_by(
            habito_id=habito.id, data=hoje).first()
        if not existe:
            novo = RegistroHabito(data=hoje)
            novo.habito_id = habito.id
            db.session.add(novo)
    db.session.commit()


def registrar_snapshots_ultima_semana(usuario_id):
    hoje = date.today()
    for n in range(6, -1, -1):
        dia = hoje - timedelta(days=n)
        if not HistoricoPendencias.query.filter_by(usuario_id=usuario_id, data=dia).first():
            registrar_snapshot_pendencias(usuario_id, dia)
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
            usuario = Usuario()
            usuario.nome = nome
            usuario.senha = senha
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
    tarefas = usuario.tarefas if usuario else []
    habitos = usuario.habitos if usuario else []
    if not HistoricoPendencias.query.filter_by(usuario_id=usuario_id, data=date.today()).first():
        registrar_snapshot_pendencias(usuario_id, date.today())
    return render_template("index.html", usuario=usuario, tarefas=tarefas, habitos=habitos, aba="dashboard")


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
    titulo = request.form["titulo"]
    prazo = request.form.get("prazo")
    if not prazo:
        flash("Por favor, preencha o prazo da tarefa.", "warning")
        return redirect(url_for("tarefas"))
    usuario_id = session.get("usuario_id")
    usuario = Usuario.query.get(usuario_id)
    tarefa = Tarefa()
    tarefa.titulo = titulo
    tarefa.prazo = datetime.strptime(prazo, "%Y-%m-%d") if prazo else None
    tarefa.data_entrega = datetime.now()
    tarefa.usuario_id = usuario_id
    db.session.add(tarefa)
    db.session.commit()
    return redirect(url_for("tarefas"))


@app.route("/concluir_tarefa/<int:id>")
def concluir_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    tarefa.concluir()
    db.session.commit()
    historico = HistoricoAtividade()
    historico.usuario_id = tarefa.usuario_id
    historico.tipo = 'tarefa'
    historico.data = date.today()
    historico.titulo = tarefa.titulo
    db.session.add(historico)
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
    habito = Habito()
    habito.titulo = titulo
    habito.usuario_id = usuario_id
    db.session.add(habito)
    db.session.commit()
    renovar_registros_habitos(usuario_id)
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
    historico = HistoricoAtividade()
    historico.usuario_id = habito.usuario_id
    historico.tipo = 'habito'
    historico.data = hoje
    historico.titulo = habito.titulo
    db.session.add(historico)
    db.session.commit()
    snap = HistoricoPendencias.query.filter_by(
        usuario_id=habito.usuario_id, data=hoje).first()
    if snap:
        db.session.delete(snap)
        db.session.commit()
    registrar_snapshot_pendencias(habito.usuario_id, hoje)
    return redirect(url_for("habitos"))


@app.route("/remover_habito/<int:id>")
def remover_habito(id):
    habito = Habito.query.get_or_404(id)
    db.session.delete(habito)
    db.session.commit()
    return redirect(url_for("habitos"))


@app.route("/lembretes_pendentes")
def lembretes_pendentes():
    usuario_id = session.get("usuario_id")
    hoje = date.today()
    # Tarefas pendentes
    tarefas = Tarefa.query.filter_by(
        usuario_id=usuario_id, status='pendente').all()
    # Hábitos pendentes do dia
    registros = RegistroHabito.query.join(Habito).filter(
        Habito.usuario_id == usuario_id,
        RegistroHabito.data == hoje,
        RegistroHabito.concluido == False
    ).all()
    habitos = [r.habito.titulo for r in registros]
    return jsonify({
        "tarefas": [
            {
                "titulo": t.titulo,
                "prazo": t.prazo.strftime('%d/%m/%Y') if t.prazo else ""
            }
            for t in tarefas
        ],
        "habitos": habitos
    })


@app.route("/dados_grafico")
def dados_grafico():
    usuario_id = session.get("usuario_id")
    hoje = date.today()
    renovar_registros_habitos(usuario_id)

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
    hoje = date.today()
    dias = [(hoje - timedelta(days=n)) for n in range(6, -1, -1)]
    dias_str = [d.strftime("%Y-%m-%d") for d in dias]
    tarefas_concluidas = []
    tarefas_pendentes = []
    habitos_concluidos = []
    habitos_pendentes = []

    for dia in dias:
        snap = HistoricoPendencias.query.filter_by(
            usuario_id=usuario_id, data=dia).first()
        if snap:
            tarefas_pendentes.append(snap.tarefas_pendentes)
            habitos_pendentes.append(snap.habitos_pendentes)
            habitos_concluidos.append(snap.habitos_concluidos)
        else:
            tarefas_pendentes.append(0)
            habitos_pendentes.append(0)
            habitos_concluidos.append(0)

        # Tarefas concluídas no dia (linha azul)
        concluidas = HistoricoAtividade.query.filter_by(
            usuario_id=usuario_id, tipo='tarefa', data=dia
        ).count()
        tarefas_concluidas.append(concluidas)

        # # Hábitos concluídos no dia (linha verde)
        # registros_concluidos = RegistroHabito.query.join(Habito).filter(
        #     Habito.usuario_id == usuario_id,
        #     RegistroHabito.data == dia,
        #     RegistroHabito.concluido == True
        # ).count()
        # habitos_concluidos.append(registros_concluidos)

    return jsonify({
        "dias": dias_str,
        "tarefas": tarefas_concluidas,
        "tarefas_pendentes": tarefas_pendentes,
        "habitos_concluidos": habitos_concluidos,
        "habitos_pendentes": habitos_pendentes
    })


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
