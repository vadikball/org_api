"""postgres session for SQLAlchemy."""

from typing import Callable

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool.impl import AsyncAdaptedQueuePool

from src.core.settings import app_settings

AsyncSessionFactory = Callable[..., AsyncSession]
session_factory_cache: AsyncSessionFactory | None = None


engine: AsyncEngine = create_async_engine(
    app_settings.POSTGRES_DSN, poolclass=AsyncAdaptedQueuePool, plugins=["geoalchemy2"]
)


async def build_db_session_factory() -> AsyncSessionFactory:
    await verify_db_connection(engine)

    return async_sessionmaker(bind=engine, expire_on_commit=False)


async def verify_db_connection(db_engine: AsyncEngine) -> None:
    connection = await db_engine.connect()
    await connection.close()


async def close_db_connections() -> None:
    await engine.dispose()
