from pydantic import BaseModel
from typing import Optional


class Dog(BaseModel):
    raca: str
    tempo_vida: str
    descricao: str 
    foto: str

class UserCreate(BaseModel):
    email: str
    name: str
    password: str
    admin: bool
