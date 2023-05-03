from pydantic import BaseModel
from typing import Optional


class BookCreate(BaseModel):
    title: str
    author: str
    year: int


class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    year: Optional[int]


class BookSchema(BaseModel):
    id: int
    title: str
    author: str
    year: int

    class Config:
        orm_mode = True

