import pytest
from sqlalchemy import text
from myOrm.database import sessionmanager


# --------------------------------------------------------------------
# — Tests
# --------------------------------------------------------------------
@pytest.mark.asyncio
async def test_database_connection():
    """Test that we can connect to the database."""
    async with sessionmanager.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        assert result.scalar() == 1


@pytest.mark.asyncio
async def test_session_rollback(db_session):
    """Test that session rollback works correctly."""
    # Create a test table and insert data
    await db_session.execute(text("DROP TABLE IF EXISTS test"))
    await db_session.execute(text("CREATE TABLE test (id INTEGER PRIMARY KEY)"))
    await db_session.execute(text("INSERT INTO test VALUES (1)"))

    # Verify data was inserted
    result = await db_session.execute(text("SELECT COUNT(*) FROM test"))
    assert result.scalar() == 1
    
    # After the test, our fixture rollback will clean up for the next one
    await db_session.rollback()


@pytest.mark.asyncio
async def test_concurrent_sessions():
    """Test that multiple sessions can be created and used."""
    results = []
    for i in range(3):
        async with sessionmanager.session() as session:
            result = await session.execute(
                text("SELECT :num"), {"num": i}
            )
            results.append(result.scalar())
    assert results == [0, 1, 2]
