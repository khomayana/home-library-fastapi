from fastapi import APIRouter, HTTPException
from sqlmodel import select
from ..models import Book, BookCreate, BookPublic, BookPublicWithAuthor, BookUpdate
from ..dependencies import SessionDep

router = APIRouter()

@router.post("/books/", response_model=BookPublic)
def create_book(book:BookCreate, session: SessionDep):
    db_book = Book.model_validate(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@router.get("/books", response_model=list[BookPublicWithAuthor])
def read_books(session: SessionDep):
    books = session.exec(
        select(Book)
    ).all()
    return books


@router.get("/books/{book_id}", response_model=BookPublicWithAuthor)
def read_book(session: SessionDep, book_id: int):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.patch("/books/{book_id}", response_model=BookPublic)
def update_book(session: SessionDep, book_id: int, book:BookUpdate):
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    book_data = book.model_dump(exclude_unset=True)
    db_book.sqlmodel_update(book_data)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@router.delete("/books/{book_id}")
def delete_book(session: SessionDep, book_id:int):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return {"status": "Deleted"}