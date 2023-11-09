from core.configs import settings
from core.database import engine
from models import __all_models

async def create_table() -> None:
  print("Criando tabelas")
  async with engine.begin() as conn:
    await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
    
    await conn.run_sync(settings.DBBaseModel.metadata.create_all)
    
  print("Tabelas criadas")
  
if __name__ == '__main__':
  import asyncio
  asyncio.run(create_table())