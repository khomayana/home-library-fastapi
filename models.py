from enum import Enum

from sqlmodel import Field, Relationship, SQLModel


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