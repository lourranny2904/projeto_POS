from pydantic import BaseModel
from typing import Optional
from datetime import date


class AdminBase(BaseModel):
    nome: str
    email: str
    senha: str
    ong: str


class Admin(AdminBase):
    id: int


class DoadorBase(BaseModel):
    nome: str
    email: str
    telefone: str
    senha: str


class Doador(DoadorBase):
    id: int


class CampanhaBase(BaseModel):
    titulo: str
    descricao: str
    meta_financeira: str
    meta_itens: str
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    status: bool


class Campanha(CampanhaBase):
    id: int


class CategoriaBase(BaseModel):
    nome: str


class Categoria(CategoriaBase):
    id: int


class DoacaoBase(BaseModel):
    id_doador: int
    id_campanha: int
    tipo_doacao: str
    tipo_item: Optional[str] = None
    quantidade: Optional[int] = None
    valor: Optional[float] = None
    data_doacao: date


class Doacao(DoacaoBase):
    id: int


class RelatorioBase(BaseModel):
    id_campanha: Optional[int] = None
    data_referencia: Optional[date] = None
    total: Optional[float] = None
    total_itens_doados: int
    meta_comparativo: str


class Relatorio(RelatorioBase):
    id: int
