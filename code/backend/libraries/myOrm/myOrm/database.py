import contextlib
from myOrm import Config
from typing import Any, AsyncIterator, AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class DatabaseSessionManager:
    def __init__(self, engine_kwargs: dict[str, Any] = None):
        if engine_kwargs is None:
            engine_kwargs = {}
        
        # Configure connection pooling
        engine_kwargs.update({
            "pool_size": 5,  # Reduced pool size for tests
            "max_overflow": 2,  # Reduced overflow for tests
            "pool_timeout": 5,  # Shorter timeout for tests
            "pool_recycle": 300,  # Recycle connections after 5 minutes
            "pool_pre_ping": True,  # Enable connection health checks
            "echo": Config.ECHO_SQL,  # Move echo here
        })
        
        self._engine = create_async_engine(Config.DATABASE_URL, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine,
            expire_on_commit=False
        )

    @property
    def engine(self):
        return self._engine

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Create a single instance of the session manager
sessionmanager = DatabaseSessionManager()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a database session.
    
    This function should be used with FastAPI's Depends() for dependency injection.
    The session will be automatically closed after the request is complete.
    """
    async with sessionmanager.session() as session:
        yield session
    