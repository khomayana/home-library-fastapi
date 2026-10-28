from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import create_engine, SQLModel, Session, Field, select, Relationship
from typing import Annotated
from enum import Enum

class AuthorBase(SQLModel):
    first_name: str = Field(index=True)
    last_name:str = Field(index=True)

class Author(AuthorBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    books: list["Book"] = Relationship(back_populates="author")

class AuthorCreate(AuthorBase):
    pass

class AuthorPublic(AuthorBase):
    id: int

class AuthorUpdate(SQLModel):
    first_name: str | None = None
    last_name:str | None = None

class StatusOptions(str, Enum):
    UNREAD="unread"
    READING="reading"
    READ="read"

class BookBase(SQLModel):
    name: str = Field(index=True)
    status: StatusOptions = Field(default="unread")
    rating: float | None = Field(default=None, ge=0, le=5)
    review: str | None = Field(default=None)

    author_id: int | None = Field(default=None, foreign_key="author.id")

class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True)  

    author: Author | None = Relationship(back_populates="books")

class BookCreate(BookBase):
    pass

class BookPublic(BookBase):
    id: int

class BookUpdate(SQLModel):
    name: str | None = None
    status: StatusOptions | None = None
    rating: float | None = None
    review: str | None = None
    author_id: int | None = None

class BookPublicWithAuthor(BookPublic):
    author: AuthorPublic | None = None

class AuthorPublicWithBooks(AuthorPublic):
    books: list[BookPublic] = []

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/books/", response_model=BookPublic)
def create_book(book:BookCreate, session: SessionDep):
    db_book = Book.model_validate(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@app.get("/books/", response_model=list[BookPublicWithAuthor])
def read_books(session: SessionDep):
    books = session.exec(
        select(Book)
    ).all()
    return books

@app.get("/books/{book_id}", response_model=BookPublicWithAuthor)
def read_book(session: SessionDep, book_id: int):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.patch("/books/{book_id}", response_model=BookPublic)
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

@app.delete("/books/{book_id}")
def delete_book(session: SessionDep, book_id:int):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return {"status": "Deleted"}


@app.post("/authors/", response_model=AuthorPublic)
def create_author(session:SessionDep, author: AuthorCreate):
    db_author = Author.model_validate(author)
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author

@app.get("/authors", response_model=list[AuthorPublicWithBooks])
def read_authors(session: SessionDep):
    authors = session.exec(
        select(Author)
    ).all()
    return authors

@app.get("/authors/{author_id}", response_model=AuthorPublicWithBooks)
def read_author(session:SessionDep, author_id:int):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@app.patch("/authors/{author_id}", response_model=AuthorPublic)
def update_author(session: SessionDep, author_id: int, author: AuthorUpdate):
    db_author = session.get(Author, author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    author_data = author.model_dump(exclude_unset=True)
    db_author.sqlmodel_update(author_data)
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author

@app.delete("/authors/{author_id}")
def delete_author(session:SessionDep, author_id: int):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    session.delete(author)
    session.commit()
    return {"status": "deleted"}

    