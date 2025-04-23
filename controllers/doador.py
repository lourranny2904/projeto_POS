from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user
from datetime import datetime
from database import db  # Certifique-se de ter inicializado o SQLAlchemy aqui
from models import Doador, Doacao, Campanha  # Importar os modelos necessários

doador_bp = Blueprint('doador', __name__, template_folder='templates')

@doador_bp.route('/indexdoador')
@login_required
def indexdoador():
    return render_template('doador/indexdoador.html')

@doador_bp.route('/cadastrodoador', methods=['GET', 'POST'])
def cadastrodoador():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        senha = request.form['senha']
        hashed_senha = generate_password_hash(senha)

        novo_doador = Doador(
            nome=nome,
            email=email,
            telefone=telefone,
            senha=hashed_senha
        )

        try:
            db.session.add(novo_doador)
            db.session.commit()
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('auth.login'))  # Redireciona para a página de login
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar: {e}', 'error')
    
    return render_template('doador/cadastro_doador.html')

@doador_bp.route('/itens_doacao', methods=['GET', 'POST'])
@login_required
def itens_doacao():
    if request.method == 'POST':
        id_campanha = request.form.get('id_campanha')
        valor = request.form.get('valor')
        data_doacao = request.form.get('data_doacao')
        data_doacao = datetime.strptime(data_doacao, '%Y-%m-%d').date()

        nova_doacao = Doacao(
            id_doador=current_user.id,
            id_campanha=int(id_campanha),
            valor=float(valor),
            data_doacao=data_doacao
        )

        try:
            db.session.add(nova_doacao)
            db.session.commit()
            flash('Doação registrada com sucesso!')
        except Exception as e:
            db.session.rollback()
            flash('Erro ao registrar a doação. Tente novamente mais tarde.')

    campanhas = Campanha.query.all()  # Obtém todas as campanhas
    return render_template('doador/itens_doacoes.html', campanhas=campanhas)

@doador_bp.route('/listar', methods=['GET'])
@login_required
def listar():
    doadores = Doador.query.filter_by(admin_id=current_user.id).all()
    return render_template('doador/listar_doadores.html', doadores=doadores)