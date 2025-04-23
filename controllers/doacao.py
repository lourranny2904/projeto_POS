from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from database import db  # Certifique-se de ter inicializado o SQLAlchemy aqui
from models import Doacao, Campanha  # Importar as classes Doacao e Campanha do modelo

doacao_bp = Blueprint('doacao', __name__, template_folder='templates')

@doacao_bp.route('/itens_doacao', methods=['GET', 'POST'])
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
            print(f"Erro ao registrar a doação: {e}")  # Para depuração
            flash('Erro ao registrar a doação. Tente novamente mais tarde.')
            return redirect(url_for('doacao.itens_doacao'))

    campanhas = Campanha.query.all()  # Obtém todas as campanhas
    return render_template('doacao/cadastro_itens_doacao.html', campanhas=campanhas)

@doacao_bp.route('/listar_doacoes', methods=['GET'])
@login_required
def listar_doacoes():
    doacoes = db.session.query(
        Doacao.valor,
        Doacao.data_doacao,
        Doador.nome.label('doador_nome'),
        Campanha.titulo.label('campanha_titulo')
    ).join(Doador, Doacao.id_doador == Doador.id) \
     .join(Campanha, Doacao.id_campanha == Campanha.id) \
     .filter(Campanha.admin_id == current_user.id) \
     .all()
    
    return render_template('doacao/listar_doacoes.html', doacoes=doacoes)