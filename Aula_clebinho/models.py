from pydantic import BaseModel
from typing import Optional


class Curso(BaseModel):
    id: Optional[int] = None
    name: str
    aulas: float 
    horas: float
    instrutor: str 