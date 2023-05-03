from fastapi import FastAPI, HTTPException, Depends

from src.models import Book
from src.database import async_session
from src.schemas import BookSchema, BookCreate, BookUpdate
from src.users import user
from src.auth import authentication, schemas
from src.auth.dependencies import get_current_user
import uvicorn

app = FastAPI()

app.include_router(user.router)
app.include_router(authentication.router)


@app.get("/users/me")
async def read_current_user(current_user: schemas.TokenData = Depends(get_current_user)):
    return {"username": current_user.username}


@app.post("/books/", response_model=BookSchema)
async def create_book(book: BookCreate):
    async with async_session() as session:
        db_book = Book(**book.dict())
        session.add(db_book)
        await session.commit()
        await session.refresh(db_book)
        return db_book


@app.get("/books/{book_id}", response_model=BookSchema)
async def read_book(book_id: int):
    async with async_session() as session:
        db_book = await session.get(Book, book_id)
        if db_book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return db_book


@app.put("/books/{book_id}", response_model=BookSchema)
async def update_book(book_id: int, book: BookUpdate):
    async with async_session() as session:
        db_book = await session.get(Book, book_id)
        if db_book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        for field, value in book.dict(exclude_unset=True).items():
            setattr(db_book, field, value)
        session.add(db_book)
        await session.commit()
        await session.refresh(db_book)
        return db_book


@app.delete("/books/{book_id}", response_model=BookSchema)
async def delete_book(book_id: int):
    async with async_session() as session:
        db_book = await session.get(Book, book_id)
        if db_book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        session.delete(db_book)
        await session.commit()
        return db_book


if __name__ == '__main__':
    uvicorn.run(app)
