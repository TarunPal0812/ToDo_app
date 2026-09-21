from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config.config import setting


engine = create_async_engine(
    url= setting.DATABASE_URL
)

AsyncSessionLocal = async_sessionmaker(
    bind= engine
)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

