from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///C:\\Users\\ct67ca\\Desktop\\fastapi-studies\\API_Desafio\\database.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()