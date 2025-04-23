from flask import Flask, render_template
from controllers.campanha import campanha_bp
from controllers.doacao import doacao_bp
from controllers.doador import doador_bp
from auth.bp import auth_bp, login_manager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'dificil'

# Configurações para SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_banco.db'  # Caminho do banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(doacao_bp)
app.register_blueprint(doador_bp)
app.register_blueprint(campanha_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)