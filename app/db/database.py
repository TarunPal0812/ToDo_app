from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config.config import setting


engine = create_async_engine(
    url= setting.DATABASE_URL,
    echo = True
)

AsyncSessionLocal = async_sessionmaker(
    bind= engine,
    class_= AsyncSession,
    expire_on_commit= False
)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


async def creat_table():
    from app.models.todo import Todo

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
