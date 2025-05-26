from fastapi import FastAPI
from controllers import doacoes, campanhas
from auth import auth

app = FastAPI()

app.include_router(doacoes.router)  
app.include_router(campanhas.router) 
app.include_router(auth.router) 
