from fastapi import APIRouter, HTTPException
from sqlmodel import select
from ..models import Author, AuthorCreate, AuthorUpdate, AuthorPublic, AuthorPublicWithBooks
from ..dependencies import SessionDep

router = APIRouter()

@router.post("/authors/", response_model=AuthorPublic)
def create_author(session:SessionDep, author: AuthorCreate):
    db_author = Author.model_validate(author)
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author

@router.get("/authors", response_model=list[AuthorPublicWithBooks])
def read_authors(session: SessionDep):
    authors = session.exec(
        select(Author)
    ).all()
    return authors

@router.get("/authors/{author_id}", response_model=AuthorPublicWithBooks)
def read_author(session:SessionDep, author_id:int):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.patch("/authors/{author_id}", response_model=AuthorPublic)
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

@router.delete("/authors/{author_id}")
def delete_author(session:SessionDep, author_id: int):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    session.delete(author)
    session.commit()
    return {"status": "deleted"}