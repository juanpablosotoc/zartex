from fastapi import HTTPException, Header, Depends
from .core import DBSessionDep
from helper import Encryption
from orm import Client, get_db_session
from sqlalchemy import select
from jwt.exceptions import InvalidTokenError


async def validate_is_authenticated(
        token: str = Header(...), 
        db_async_gen: DBSessionDep = Depends(get_db_session)
    ) -> Client:
    db = await db_async_gen.__anext__()
    try:
        payload = Encryption.verify_token(token)
        user = await db.execute(select(Client).where(Client.id == payload["user_id"]))
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
async def validate_is_admin(user: Client = Depends(validate_is_authenticated)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="You are not authorized to access this resource")
    return user
