from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from sqlalchemy import text  # Importar text para executar comandos SQL
import os

# Carregar variáveis de ambiente
load_dotenv('.env')

# Configurações do Flask e SQLite
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLITE_URI', 'sqlite:///db_banco.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def banco(banco_dados):
    with app.app_context():
        with open(banco_dados, 'r') as file:
            sql = file.read()
            comandos_raw = sql.split(';')
            commands = [comando.strip() for comando in comandos_raw if comando.strip()]

            # Usar a conexão para executar os comandos SQL
            with db.engine.connect() as connection:
                for command in commands:
                    connection.execute(text(command))  # Envolve o comando com text()
        db.session.commit()  # Mantenha isso se estiver fazendo operações que precisam de commit

if __name__ == "__main__":
    caminho_sql = os.path.join(os.path.dirname(__file__), 'mysql.sql')
    banco(caminho_sql)
    print("Banco de dados e tabelas inicializados com sucesso!")

# Adicione esta linha para exportar db
__all__ = ['app', 'db']