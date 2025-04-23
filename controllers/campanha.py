from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from database import db  # Certifique-se de ter inicializado o SQLAlchemy aqui
from datetime import datetime
from models import Campanha  # Importar a classe Campanha do modelo

campanha_bp = Blueprint('campanha', __name__, template_folder='templates')

@campanha_bp.route('/campanhas', methods=['GET', 'POST'])
@login_required
def campanhas():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        meta_financeira = request.form.get('meta_financeira')
        data_inicio = request.form.get('data_inicio')
        data_fim = request.form.get('data_fim')
        status = request.form.get('status')

        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()

        nova_campanha = Campanha(
            titulo=titulo,
            descricao=descricao,
            meta_financeira=meta_financeira,
            data_inicio=data_inicio,
            data_fim=data_fim,
            status=status,
            admin_id=current_user.id
        )
        
        db.session.add(nova_campanha)
        db.session.commit()

        flash('Campanha criada com sucesso!')
        return redirect(url_for('campanha.listar_campanhas'))

    return render_template('campanha/cadastro_campanhas.html')

@campanha_bp.route('/listar_campanhas', methods=['GET'])
@login_required
def listar_campanhas():
    data_inicial = request.args.get('data-inicial')
    data_final = request.args.get('data-final')

    if current_user.is_admin():
        campanhas = Campanha.query.all()
    else:
        campanhas = Campanha.query.filter_by(admin_id=current_user.id).all()

    if data_inicial and data_final:
        campanhas = [campanha for campanha in campanhas if campanha.data_inicio >= data_inicial and campanha.data_fim <= data_final]
    elif data_inicial:
        campanhas = [campanha for campanha in campanhas if campanha.data_inicio >= data_inicial]
    elif data_final:
        campanhas = [campanha for campanha in campanhas if campanha.data_fim <= data_final]

    # Renderiza o template baseado no tipo de usuário
    if current_user.is_admin():
        return render_template('campanha/listar_campanhas.html', campanhas=campanhas)
    else:
        return render_template('campanha/listar_campanhas_doador.html', campanhas=campanhas)

@campanha_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    campanha = Campanha.query.get(id)

    if not campanha:
        flash('Campanha não encontrada.')
        return redirect(url_for('campanha.listar_campanhas'))

    if request.method == 'POST':
        campanha.titulo = request.form.get('titulo')
        campanha.descricao = request.form.get('descricao')
        campanha.meta_financeira = request.form.get('meta_financeira')
        campanha.data_inicio = datetime.strptime(request.form.get('data_inicio'), '%Y-%m-%d').date()
        campanha.data_fim = datetime.strptime(request.form.get('data_fim'), '%Y-%m-%d').date()
        campanha.status = request.form.get('status')

        db.session.commit()
        
        flash('Campanha atualizada com sucesso!')
        return redirect(url_for('campanha.listar_campanhas'))

    return render_template('campanha/editar_campanha.html', campanha=campanha)

@campanha_bp.route('/excluir/<int:id>', methods=['POST'])
@login_required
def excluir(id):
    campanha = Campanha.query.get(id)

    if campanha:
        # Excluir doações associadas
        db.session.query(Doador).filter_by(id_campanha=id).delete()
        
        # Excluir a campanha
        db.session.delete(campanha)
        db.session.commit()

        flash('Campanha e doações associadas excluídas com sucesso!', 'success')
    else:
        flash('Campanha não encontrada.')

    return redirect(url_for('campanha.listar_campanhas'))