from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from backend.database import Database
from backend.external_apis import get_currency_rates, get_stock_quotes, get_esports_games


app = FastAPI()
db = Database()

# Modelos Pydantic
class Usuario(BaseModel):
    nome: str
    idade: int
    email: str
    senha: str
    numero: Optional[str] = None
    salario: Optional[float] = None
    profissao: Optional[str] = None

class Transacao(BaseModel):
    valor: float
    descricao: str
    data: date
    categoria_id: int
    usuario_id: int

class CustoGanhoFixo(BaseModel):
    valor: float
    descricao: str
    categoria_id: int
    usuario_id: int
    tipo: str
    dia: int

class Aposta(BaseModel):
    jogo: str
    valor_apostado: float
    resultado: str
    data: date
    usuario_id: int

class Investimento(BaseModel):
    valor: float
    tipo: str
    descricao: str
    data: date
    usuario_id: int

# Endpoints de Usuários
@app.post("/usuarios/", response_model=dict)
async def criar_usuario(usuario: Usuario):
    try:
        usuario_id = db.insert_usuario(usuario.nome, usuario.idade, usuario.email, usuario.senha)
        if usuario.numero or usuario.salario or usuario.profissao:
            db.update_usuario(usuario_id, usuario.numero, usuario.salario, usuario.profissao)
        return {"id": usuario_id, "message": "Usuário criado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login/")
async def login(email: str, senha: str):
    usuario = db.autenticar_usuario(email, senha)
    if usuario:
        return {"usuario_id": usuario[0], "nome": usuario[1]}
    raise HTTPException(status_code=401, detail="Email ou senha incorretos")

# Endpoints de Transações
@app.post("/transacoes/", response_model=dict)
async def adicionar_transacao(transacao: Transacao):
    try:
        db.insert_transacao(transacao.valor, transacao.descricao, transacao.data, transacao.categoria_id, transacao.usuario_id)
        return {"message": "Transação adicionada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/transacoes/{usuario_id}", response_model=List[dict])
async def listar_transacoes(usuario_id: int):
    transacoes = db.get_transacoes(usuario_id)
    return [{"id": t[0], "valor": t[1], "descricao": t[2], "data": t[3], "categoria": t[4], "tipo": t[5]} for t in transacoes]

@app.delete("/transacoes/{transacao_id}", response_model=dict)
async def excluir_transacao(transacao_id: int):
    try:
        db.delete_transacao(transacao_id)
        return {"message": "Transação excluída com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoints de Custos/Ganhos Fixos
@app.post("/custos_ganhos_fixos/", response_model=dict)
async def adicionar_custo_ganho_fixo(custo: CustoGanhoFixo):
    try:
        db.insert_custo_ganho_fixo(custo.valor, custo.descricao, custo.categoria_id, custo.usuario_id, custo.tipo, custo.dia)
        return {"message": "Custo/Ganho fixo adicionado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/custos_ganhos_fixos/{usuario_id}", response_model=List[dict])
async def listar_custos_ganhos_fixos(usuario_id: int):
    fixos = db.get_custos_ganhos_fixos(usuario_id)
    return [{"id": f[0], "valor": f[1], "descricao": f[2], "dia": f[3], "categoria": f[4], "tipo": f[5]} for f in fixos]

# Endpoints de Apostas
@app.post("/apostas/", response_model=dict)
async def adicionar_aposta(aposta: Aposta):
    try:
        db.insert_aposta(aposta.jogo, aposta.valor_apostado, aposta.resultado, aposta.data, aposta.usuario_id)
        return {"message": "Aposta adicionada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/apostas/{usuario_id}", response_model=List[dict])
async def listar_apostas(usuario_id: int):
    apostas = db.get_apostas(usuario_id)
    return [{"id": a[0], "jogo": a[1], "valor_apostado": a[2], "resultado": a[3], "data": a[4]} for a in apostas]

# Endpoints de Investimentos
@app.post("/investimentos/", response_model=dict)
async def adicionar_investimento(investimento: Investimento):
    try:
        db.insert_investimento(investimento.valor, investimento.tipo, investimento.descricao, investimento.data, investimento.usuario_id)
        return {"message": "Investimento adicionado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/investimentos/{usuario_id}", response_model=List[dict])
async def listar_investimentos(usuario_id: int):
    investimentos = db.get_investimentos(usuario_id)
    return [{"id": i[0], "valor": i[1], "tipo": i[2], "descricao": i[3], "data": i[4]} for i in investimentos]

@app.delete("/investimentos/{investimento_id}", response_model=dict)
async def excluir_investimento(investimento_id: int):
    try:
        db.delete_investimento(investimento_id)
        return {"message": "Investimento excluído com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoints de Categorias
@app.get("/categorias/", response_model=List[dict])
async def listar_categorias():
    categorias = db.get_categorias()
    return [{"id": c[0], "nome": c[1], "tipo": c[2]} for c in categorias]

# Endpoints de Resumos e Cotações
@app.get("/resumo_semanal/{usuario_id}", response_model=dict)
async def resumo_semanal(usuario_id: int):
    resumo = db.get_resumo_semanal(usuario_id)
    return {
        "total_receitas": resumo[0][1] if resumo[0] else 0,
        "total_despesas": resumo[1][1] if resumo[1] else 0,
        "total_apostas_ganhas": resumo[2][1] if resumo[2] else 0,
        "total_apostas_perdidas": resumo[3][1] if resumo[3] else 0
    }

@app.get("/cotacoes/", response_model=dict)
async def cotacoes():
    try:
        moedas = get_currency_rates()
        bolsas = get_stock_quotes()
        return {"moedas": moedas, "bolsas": bolsas}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/jogos_esports/", response_model=List[dict])
async def jogos_esports():
    try:
        jogos = get_esports_games()
        return jogos
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))