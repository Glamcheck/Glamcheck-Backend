from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from glamcheck.settings import settings

engine = create_async_engine(settings.db_connection_string)
async_session = async_sessionmaker(bind=engine)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
