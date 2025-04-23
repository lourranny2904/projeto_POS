from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()  # Apenas declare a variável aqui

class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    senha = db.Column(db.String, nullable=False)
    ong = db.Column(db.String, nullable=False)

    def get_id(self):
        return self.id

class Doador(UserMixin, db.Model):
    __tablename__ = 'doadores'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    telefone = db.Column(db.String, nullable=False)
    senha = db.Column(db.String, nullable=False)

    def get_id(self):
        return self.id

def obter_admin(email):
    admin_data = Admin.query.filter_by(email=email).first()
    return admin_data

def obter_doador(email):
    doador_data = Doador.query.filter_by(email=email).first()
    return doador_data