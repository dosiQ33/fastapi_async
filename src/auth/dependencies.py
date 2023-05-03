from datetime import datetime

from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select

from src.database import get_async_session, AsyncSession
from src.users import models
from .schemas import TokenData
from .utils import JWT_SECRET_KEY, ALGORITHM

reusable_oauth = OAuth2PasswordBearer(
    tokenUrl="login",
    scheme_name="JWT"
)


async def get_user(db: AsyncSession, username: str):
    users = await db.execute(select(models.User).where(models.User.name == username))
    user = users.scalar()
    return user


async def get_current_user(token: str = Depends(reusable_oauth),
                           session: AsyncSession = Depends(get_async_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user = get_user(session, username=username)
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise credentials_exception
        if user is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return token_data
