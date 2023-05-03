from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class User(BaseModel):
    name: str
    surname: str
    middle_name: Optional[str]
    password: str = Field(title="Password must be at least 6 characters in length", min_length=6)
    email: EmailStr
    phone: str


class ShowUser(BaseModel):
    name: str
    surname: str
    middle_name: Optional[str]
    email: EmailStr
    phone: str

    class Config:
        orm_mode = True
