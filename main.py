from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel
from enum import Enum

class StatusOption(str, Enum):
    option_unread="unread"
    option_read = "read"

class BookModel(BaseModel):
    book_id: int
    book_name: str
    author_first_name: str
    author_last_name: str
    status: StatusOption 
    rate: float = 0
    book_review: str | None = None
    

class BookModelIn(BaseModel):
    book_name: str
    author_first_name: str
    author_last_name: str
    status: StatusOption
    rate: float=0
    book_review: str | None = None

class BookModelUpdate(BaseModel):
    status: StatusOption
    rate: float=0
    book_review: str | None = None

app = FastAPI()

db_books = [
    {
        "book_id": 1,
        "book_name":"Fourth wing",
        "author_first_name":"Rebecca",
        "author_last_name":"Yarros",
        "status":"read",
        "rate":5,
        "book_review": "Fascinating book"
    },
    {
        "book_id": 2,
        "book_name":"Iron Flame",
        "author_first_name":"Rebecca",
        "author_last_name":"Yarros",
        "status":"read",
        "rate":5,
        "book_review": "Like this"
    },
    {
        "book_id": 3,
        "book_name":"Onyx Storm",
        "author_first_name":"Rebecca",
        "author_last_name":"Yarros",
        "status":"read",
        "rate":5,
        "book_review": "Fascinating book"
    },
    {
        "book_id": 4,
        "book_name":"Binding 13",
        "author_first_name":"Chloe",
        "author_last_name":"Walsh",
        "status":"read",
        "rate":5,
        "book_review": "Fascinating book"
    },  

    
]

@app.get("/")
async def root():
    return db_books


@app.get("/books/{id}")
async def get_book_by_id(id: int)-> BookModel:
    for book in db_books:
        if book["book_id"] == id:
            return book
    raise HTTPException(status_code=404, detail="Book is not found")

@app.get("/books/")
async def get_books_by_name(name:str)->list[BookModel]:
    result_list = []
    for book in db_books:
        if name.lower() in book["book_name"].lower():
            result_list.append(book)
    if len(result_list) <=0:
        raise HTTPException(status_code=404, detail="Book not found")
    return result_list

@app.get("/books_by_author/")
async def get_books_by_author(first_name:str|None =None, last_name:str|None=None) -> list[BookModel]:
    result_list = []
    for book in db_books:
        if first_name != None and first_name.lower() in book["author_first_name"].lower():
            result_list.append(book)
        if last_name != None and last_name.lower() in book["author_last_name"].lower():
            is_added_to_list = False
            for item in result_list:
                if book["book_id"] == item["book_id"]:
                    is_added_to_list = True
            if not is_added_to_list:
                result_list.append(book)
    if len(result_list) == 0:
        raise HTTPException(status_code=404, detail=f"Name {first_name if first_name != None else last_name} not found")
    return result_list

@app.post("/books/")
async def create_book(book:BookModelIn) -> BookModel:
    new_book = BookModel(
        # book_id=(db_books.model_dump()[-1]["book_id"])+1,
        book_id= db_books[-1]["book_id"]+1 if len(db_books)>0 else 1,
        book_name=book.book_name,
        author_first_name=book.author_first_name,
        author_last_name=book.author_last_name,
        status=book.status,
        rate = book.rate,
        book_review=book.book_review
    )
    #new_book is a Pydantic model and db_books is a list of dictionaries 
    # .model_dump() - converts Pydantic model to dictionary (without it type error occurs)
    db_books.append(new_book.model_dump())
    
    return new_book

@app.put("/books/{id}")
async def update_book(id:int, book_input:BookModelUpdate) -> BookModel:
    for book in db_books:
        if book["book_id"] == id:
            book["status"] = book_input.status
            book["rate"] = book_input.rate
            book["book_review"] = book_input.book_review
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id:int):
    for index,book in enumerate(db_books):
        if book["book_id"] == id:
            del db_books[index]
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail="Book not found")

                 

    