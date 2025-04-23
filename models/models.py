from sqlalchemy import Integer, String, Text, Date, ForeignKey, Float
from sqlalchemy.orm import mapped_column, relationship
from database.config import Base
from datetime import date
from flask_login import UserMixin

class Admin(Base,UserMixin):
    __tablename__ = 'admin'
    
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome = mapped_column(String, nullable=False)
    email = mapped_column(String, nullable=False, unique=True)
    senha = mapped_column(String, nullable=False)
    ong = mapped_column(String, nullable=False)
    data_criacao = mapped_column(Date, default=date.today)

    def set_password(self, password: str):
        self.senha = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.senha, password)

    def get_id(self):
        return str(self.id)


class Doador(Base, UserMixin):
    __tablename__ = 'doadores'
    
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome = mapped_column(String, nullable=False)
    email = mapped_column(String, nullable=False, unique=True)
    telefone = mapped_column(String, nullable=False)
    senha = mapped_column(String, nullable=False)
    data_criacao = mapped_column(Date, default=date.today)
    
    doacoes = relationship("Doacao", back_populates="doador")

    def set_password(self, password: str):
        self.senha = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.senha, password)

    def get_id(self):
        return str(self.id)


class Categoria(Base):
    __tablename__ = 'categorias'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome = mapped_column(String, nullable=False)



class Campanha(Base):
    __tablename__ = 'campanhas'
    
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo = mapped_column(String, nullable=False)
    descricao = mapped_column(Text, nullable=False)
    meta_financeira = mapped_column(String, nullable=False)
    meta_itens = mapped_column(String, nullable=False)
    data_inicio = mapped_column(Date)
    data_fim = mapped_column(Date)
    status = mapped_column(String, nullable=False)
    data_criacao = mapped_column(Date, default=date.today)
    categoria_id = mapped_column(Integer, ForeignKey('categorias.id'))
    
    doacoes = relationship("Doacao", back_populates="campanha")
    relatorios = relationship("Relatorio", back_populates="campanha")



class Doacao(Base):
    __tablename__ = 'doacoes'
    
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_doador = mapped_column(Integer, ForeignKey('doadores.id'), nullable=False)
    id_campanha = mapped_column(Integer, ForeignKey('campanhas.id'), nullable=False)
    tipo_doacao = mapped_column(String, nullable=False)
    tipo_item = mapped_column(String)
    quantidade = mapped_column(Integer)
    valor = mapped_column(Float)
    data_doacao = mapped_column(Date, nullable=False)
    status = mapped_column(String, default='confirmada')

    doador = relationship("Doador", back_populates="doacoes")
    campanha = relationship("Campanha", back_populates="doacoes")


class Relatorio(Base):
    __tablename__ = 'relatorios'
    
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_campanha = mapped_column(Integer, ForeignKey('campanhas.id'))
    data_referencia = mapped_column(Date)
    total = mapped_column(Float)
    total_itens_doados = mapped_column(Integer, nullable=False)
    meta_comparativo = mapped_column(String, nullable=False)

    campanha = relationship("Campanha", back_populates="relatorios")

