from typing import Optional
from pydantic import BaseModel as SchemaBaseModel

class DogSchema(SchemaBaseModel):
    id: Optional[int] = None
    raca: str
    tempo_vida: int
    descricao: str

    class Config:
        from_attributes = True