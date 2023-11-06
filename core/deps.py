from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import Session

async def get_session() -> Generator: #função vai ter como retorno um Generator
    session: AsyncSession = Session()
    try:
        yield session #é um return "sem ser return" -> ele devolve a sessão mas mantém a função viva! AGUARDE AQUI...
    finally:
        await session.close() #após utilizar a sessão com o banco, ai sim, finalizamos ela