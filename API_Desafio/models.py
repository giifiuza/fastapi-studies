from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Table, Time


class Dogs(Base):
    __tablename__ = "dogs"
    
    id = Column(Integer, primary_key=True, index=True)
    raca = Column(String)
    tempo_vida = Column(String)
    descricao = Column(String)
    foto = Column(String)
    
class User(Base):
    __tablename__ = "user"
    iduser = Column(Integer, primary_key=True, index=True)
    email = Column(Integer)
    name = Column(String)
    password = Column(String)
    admin = Column(Boolean, default=False)
