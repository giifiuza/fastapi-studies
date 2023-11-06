from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from core.configs import settings

engine: AsyncEngine = create_async_engine(settings.DB_URL)
#sessionmaker retorna uma classe!
#abre e fecha a conexão com o banco de dados!

Session: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)