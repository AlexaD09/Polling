from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config_usuario import PSSW_POSTGRE

DATABASE_URL = f"postgresql+asyncpg://postgres:{PSSW_POSTGRE}@postgres:5432/quejas_db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session: 
        yield session