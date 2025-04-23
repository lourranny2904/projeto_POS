from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from models import Admin, Doador, db  # Importando as classes e o db

auth_bp = Blueprint('auth', __name__, template_folder='templates')

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    admin = Admin.query.get(user_id)
    if admin:
        return admin

    doador = Doador.query.get(user_id)
    return doador

@auth_bp.route('/indexadmin')
@login_required
def indexadmin():
    return render_template('auth/indexadmin.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        role = request.form.get('role')

        if role == 'Admin':
            admin = Admin.query.filter_by(email=email).first()
            if admin and check_password_hash(admin.senha, senha):
                login_user(admin)
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('auth.indexadmin'))

        elif role == 'doador':
            doador = Doador.query.filter_by(email=email).first()
            if doador and check_password_hash(doador.senha, senha):
                login_user(doador)
                flash('Login realizado com sucesso!', 'success')
                return redirect(url_for('doador.indexdoador'))

        flash('Email ou senha incorretos', 'error')

    return render_template('auth/login.html')

@auth_bp.route('/cadastro_admin', methods=['GET', 'POST'])
def cadastro_admin():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        ong = request.form['ong']
        senha = request.form['senha']

        novo_admin = Admin(
            nome=nome,
            email=email,
            ong=ong,
            senha=generate_password_hash(senha)
        )

        try:
            db.session.add(novo_admin)
            db.session.commit()
            flash('Administrador cadastrado com sucesso!')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar: {e}', 'error')

    return render_template('auth/cadastro_admin.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@auth_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('auth/indexadmin.html', nome=current_user.ong)