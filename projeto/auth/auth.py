from fastapi import APIRouter, HTTPException
from models import Admin, Doador
from typing import List

router = APIRouter()

admins: List[Admin] = []
doadores: List[Doador] = []

@router.post("/auth/cadastro_admin")
def cadastro_admin(admin: Admin):
    # Verifica se já existe email cadastrado
    for a in admins:
        if a.email == admin.email:
            raise HTTPException(status_code=400, detail="Email já cadastrado")
    novo_id = len(admins) + 1
    admin.id = novo_id  # atribui o id incremental
    admins.append(admin)
    return {"msg": "Administrador cadastrado com sucesso", "id": admin.id}

@router.get("/auth/admins")
def listar_admins():
    return admins

@router.get("/auth/doadores")
def listar_doadores():
    return doadores

@router.post("/auth/cadastro_doador")
def cadastro_doador(doador: Doador):
    for d in doadores:
        if d.email == doador.email:
            raise HTTPException(status_code=400, detail="Email já cadastrado")
    novo_id = len(doadores) + 1
    doador.id = novo_id  # atribui o id incremental
    doadores.append(doador)
    return {"msg": "Doador cadastrado com sucesso", "id": doador.id}


