from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select

from src.database import async_session, get_async_session, AsyncSession
from src.users import models
from src.auth.utils import verify_password, create_access_token, create_refresh_token
from src.auth.dependencies import get_user


router = APIRouter(
    tags=['Authentication']
)


@router.post("/login", summary="used in back for authentication")
async def login(requests: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)):
    async with async_session() as session:
        # user = get_user(session, username=requests.username) # почему то пароль не передается?
        users = await session.execute(select(models.User).where(models.User.name == requests.username))
        user = users.scalar()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
        if not verify_password(requests.password, user.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password")
        return {
            "access_token": create_access_token(user.phone),
            "refresh_token": create_refresh_token(user.phone),
        }
