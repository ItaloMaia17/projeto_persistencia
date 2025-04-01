from fastapi import FastAPI
from contextlib import asynccontextmanager
from database_config import create_db_and_tables
from routes import home, dispositivo, servico, peca, tecnico

# Configuração pré-inicialização
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

# Inicialização da API
app = FastAPI(lifespan=lifespan)

app.include_router(home.router)
app.include_router(dispositivo.router)
app.include_router(servico.router)
app.include_router(peca.router)
app.include_router(tecnico.router)
