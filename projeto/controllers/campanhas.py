from fastapi import APIRouter, HTTPException
from typing import List
from models import Campanha, CampanhaBase
from datetime import date


router = APIRouter()

campanhas: List[Campanha] = []

# Listar todas as campanhas
@router.get("/campanhas", response_model=List[Campanha])
def listar_campanhas():
    return campanhas

# Buscar campanha pelo id (index + 1)
@router.get("/campanhas/{id}", response_model=Campanha)
def buscar_campanha(id: int):
    for campanha in campanhas:
        if campanha.id == id:
            return campanha
    raise HTTPException(status_code=404, detail="Campanha não encontrada")

# Criar uma campanha
@router.post("/campanhas", response_model=Campanha)
def criar_campanha(campanha_base: CampanhaBase):
    novo_id = len(campanhas) + 1
    campanha = Campanha(id=novo_id, **campanha_base.dict())
    campanhas.append(campanha)
    return campanha

# Editar uma campanha pelo id
@router.put("/campanhas/{id}", response_model=Campanha)
def editar_campanha(id: int, dados: CampanhaBase):
    for i, campanha in enumerate(campanhas):
        if campanha.id == id:
            campanhas[i] = Campanha(id=id, **dados.dict())
            return campanhas[i]
    raise HTTPException(status_code=404, detail="Campanha não encontrada")

# Excluir campanha pelo id
@router.delete("/campanhas/{id}", response_model=Campanha)
def excluir_campanha(id: int):
    for i, campanha in enumerate(campanhas):
        if campanha.id == id:
            return campanhas.pop(i)
    raise HTTPException(status_code=404, detail="Campanha não encontrada")
