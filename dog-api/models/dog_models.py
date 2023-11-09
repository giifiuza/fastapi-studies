from core.configs import settings
from sqlalchemy import Column, Integer, String

class DogModel(settings.DBBaseModel):
    __tablename__ = "cachorro"
    id: int = Column(Integer, primary_key=True, autoincrement=True, default=0)
    raca: str = Column(String(100))
    tempo_vida: int = Column(Integer)
    descricao: str = Column(String(255))