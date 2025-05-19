import pytest
import pytest_asyncio
import os
from config import Config
from sqlalchemy import text
from myOrm.database import get_db_session, sessionmanager
from myOrm.models import Base
from datetime import datetime, UTC


# Configure pytest-asyncio
def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "asyncio: mark test as async"
    )


# --------------------------------------------------------------------
# — Auto‐dispose the engine after each test to avoid "future attached
#   to a different loop" errors
# --------------------------------------------------------------------
@pytest_asyncio.fixture(autouse=True)
async def _dispose_engine():
    yield
    await sessionmanager.engine.dispose()


# --------------------------------------------------------------------
# — Create/drop tables once per session run
# --------------------------------------------------------------------
@pytest_asyncio.fixture(scope="session")
async def setup_database():
    """Create test database tables at the start, and drop them at the end."""
    async with sessionmanager.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with sessionmanager.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        

@pytest_asyncio.fixture
async def db_session(setup_database):
    """Create a fresh database session for each test."""
    async with sessionmanager.session() as session:
        try:
            # Clean up all tables before each test
            for table in reversed(Base.metadata.sorted_tables):
                try:
                    await session.execute(text(f"DELETE FROM {table.name}"))
                except Exception:
                    # Table might not exist yet, which is fine
                    pass
            await session.commit()
            
            yield session
        finally:
            await session.rollback()
            await session.close()
