from pydantic import BaseModel
from typing import Optional


class Dog(BaseModel):
    id: Optional[int] = None
    raca: str
    tempo_vida: str
    descricao: str 