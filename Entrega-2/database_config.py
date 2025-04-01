import sqlite3
from sqlalchemy import event, Engine
from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
import logging
import os

# Carrega variaveis de ambiente
load_dotenv()

# Habilita o log 
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Cria uma nova conexão
engine = create_engine(os.getenv("DATABASE_URL"))

# Cria o banco e as tabelas caso não existam
def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

# Pega a conexão criada;
def get_session() -> Session:
    return Session(engine)

# Habilita a verificação de chaves estrangeiras
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_records):
    if type(dbapi_connection) is sqlite3.Connection:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys= ON")
        cursor.close()