from typing import Annotated
from orm import get_db_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator

DBSessionDep = Annotated[AsyncGenerator[AsyncSession, None], Depends(get_db_session)]
