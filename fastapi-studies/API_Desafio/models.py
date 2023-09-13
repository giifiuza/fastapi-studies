from pydantic import BaseModel
from typing import Optional


class Cat(BaseModel):
    id: Optional[str] = None
    raca: str
    tempo_vida: str
    descricao: str 
    foto: str
    