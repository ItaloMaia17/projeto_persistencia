import sqlite3
from sqlalchemy import event, Engine
from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
import logging
import os


#carrega variaveis de ambiente
load_dotenv()

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

engine = create_engine(os.getenv(DATABASE_URL))
