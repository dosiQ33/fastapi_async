from fastapi import APIRouter, status, HTTPException
from sqlalchemy import select

from . import schemas, models
from src.database import async_session
from src.auth.utils import get_hashed_password

router = APIRouter(
    tags=['Users']
)


@router.post('/signup', status_code=status.HTTP_201_CREATED,
             response_model=schemas.ShowUser, summary="Creating a new user")
async def create_user(requests: schemas.User):
    async with async_session() as session:
        # checking if user already exists in the database
        existing_users = await session.execute(select(models.User).where(models.User.phone == requests.phone))
        existing_user = existing_users.scalar()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User with this phone number is already exists"
                                )

        new_user = models.User(name=requests.name,
                               surname=requests.surname,
                               middle_name=requests.middle_name,
                               password=get_hashed_password(requests.password),
                               email=requests.email,
                               phone=requests.phone)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
