from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from sqlmodel.ext.asyncio.session import AsyncSession
engine = create_async_engine(
    Config.DATABASE_URL,
    echo=True,
)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
# async def init_db():
#     async with engine.begin() as conn:
#         from src.db.models import User
#         await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async with async_session() as session:
        yield session