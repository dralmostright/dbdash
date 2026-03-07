from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
import socket

engine = AsyncEngine(
        create_engine (
        url=Config.DATABASE_URL,
        echo=True,
        )
    )

async def init_db():
    async with engine.begin() as conn:
        #from src.db.models import User
        #await conn.run_sync(SQLModel.metadata.create_all)
        pass
        
async def get_session() -> AsyncSession:
    Session = sessionmaker (
        bind = engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with Session() as session:
        yield session
