from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
  id: Optional[int]
  descricao: str
  valor: float
  
class Product(BaseModel):
  id: Optional[int] = None
  quantidade: int
  descricao: str
  valor: float
  