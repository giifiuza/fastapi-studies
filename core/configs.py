from pydantic.v1 import BaseSettings
from sqlalchemy.orm import declarative_base

class Settings(BaseSettings):
  """
    Configurações gerais
  """
  
  API_VI_STR: str = '/api/v1'
  DB_URL: str = 'mysql_asyncmy://root@127.0.0.1:3306/etscursos'
  
  DBBaseModel = declarative_base()
  
  class Config:
    case_sensitive = True
    
settings = Settings() 