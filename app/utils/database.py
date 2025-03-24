from sqlalchemy import Column, BigInteger, String, TIMESTAMP, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from datetime import datetime

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/postgres"

Base = declarative_base()

class BotUser(Base):
    __tablename__ = 'bot_users'

    id = Column(Integer, primary_key=True, autoincrement=True) 
    discord_id = Column(BigInteger, unique=True, nullable=False) # I wanted this to be primary SO HARD
    username = Column(String, nullable=False)
    joined_at = Column(TIMESTAMP, default=datetime.now)

engine = create_async_engine(DATABASE_URL, future=True)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
