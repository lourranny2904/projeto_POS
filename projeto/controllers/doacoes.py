from fastapi import APIRouter, HTTPException
from typing import List
from models import Doacao, DoacaoBase
from datetime import date

router = APIRouter()

doacoes: List[Doacao] = []

@router.post("/doacoes", response_model=Doacao)
def criar_doacao(doacao_base: DoacaoBase):
    novo_id = len(doacoes) + 1
    data = doacao_base.dict()
    if not data["data_doacao"]:
        data["data_doacao"] = date.today()

    nova_doacao = Doacao(id=novo_id, **data)
    doacoes.append(nova_doacao)
    return nova_doacao

@router.get("/doacoes", response_model=List[Doacao])
def listar_doacoes():
    return doacoes

@router.get("/doacoes/por-id/{id_doador}", response_model=List[Doacao])
def listar_por_id(id_doador: int):
    resultado = [d for d in doacoes if d.id_doador == id_doador]
    if not resultado:
        raise HTTPException(404, detail="Nenhuma doação encontrada para esse doador.")
    return resultado

@router.put("/doacoes/{id_doacao}", response_model=Doacao)
def editar_doacao(id_doacao: int, doacao_base: DoacaoBase):
    for i, doacao in enumerate(doacoes):
        if doacao.id == id_doacao:
            atualizada = Doacao(id=id_doacao, **doacao_base.dict())
            doacoes[i] = atualizada
            return atualizada
    raise HTTPException(404, "Doação não encontrada.")

@router.delete("/doacoes/{id_doacao}", response_model=Doacao)
def deletar_doacao(id_doacao: int):
    for i, doacao in enumerate(doacoes):
        if doacao.id == id_doacao:
            return doacoes.pop(i)
    raise HTTPException(404, "Doação não encontrada.")
