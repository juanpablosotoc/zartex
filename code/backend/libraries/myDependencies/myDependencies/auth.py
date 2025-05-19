from fastapi import HTTPException, Header, Depends
from myEncryption import Encryption
from myOrm import Client
from sqlalchemy import select
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from myOrm import get_db_session


async def validate_is_authenticated(
        db_session: AsyncSession = Depends(get_db_session),
        token: str = Header(...), 
    ) -> Client:
    try:
        payload = Encryption.verify_token(token)
        result = await db_session.execute(select(Client).where(Client.id == payload["user_id"]))
        user = result.scalar_one_or_none()

        if not user: raise HTTPException(status_code=401, detail="Invalid token")
        
        return user
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
async def validate_is_admin(user: Client = Depends(validate_is_authenticated)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="You are not authorized to access this resource")
    return user
