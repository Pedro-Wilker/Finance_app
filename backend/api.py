from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from backend.database import Database

app = FastAPI()
db = Database()

class LoginRequest(BaseModel):
    email: str
    senha: str

class Usuario(BaseModel):
    nome: str
    idade: int
    email: str
    senha: str
    numero: Optional[str] = None
    salario: Optional[float] = None
    profissao: Optional[str] = None

@app.post("/login/")
async def login(request: LoginRequest):
    usuario = db.autenticar_usuario(request.email, request.senha)
    if usuario:
        return {"usuario_id": usuario[0], "nome": usuario[1]}
    raise HTTPException(status_code=401, detail="Email ou senha incorretos")

@app.post("/usuarios/", response_model=dict)
async def criar_usuario(usuario: Usuario):
    try:
        usuario_id = db.insert_usuario(usuario.nome, usuario.idade, usuario.email, usuario.senha)
        if usuario.numero or usuario.salario or usuario.profissao:
            db.update_usuario(usuario_id, usuario.numero, usuario.salario, usuario.profissao)
        return {"id": usuario_id, "message": "Usuário criado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))