from fastapi import FastAPI, HTTPException, status, Response
from pydantic import BaseModel

class AuthorModel(BaseModel):
    author_id: int
    first_name: str
    last_name: str
    books: list[str] = []
    rate: float = 0

class AuthorModelIn(BaseModel):
    first_name: str
    last_name: str
    books: list[str]=[]
    rate: float=0

class AuthorModelUpdate(BaseModel):
    books:list[str]
    rate:float

app = FastAPI()

db_authors = [
    {
        "author_id":1,
        "first_name":"Rebecca",
        "last_name":"Yarros",
        "books":["Forth wing", "Iron Flame", "Onyx Storm"],
        "rate":5
    },
    {
        "author_id":2,
        "first_name":"Chloe",
        "last_name":"Walsh",
        "books":["Binding 13", "Keeping 13"],
        "rate":4
    }
]

@app.get("/")
async def root():
    return db_authors


@app.get("/authors/{id}")
async def get_author_by_id(id: int)-> AuthorModel:
    for author in db_authors:
        if author["author_id"] == id:
            return author
    raise HTTPException(status_code=404, detail="Author is not found")

@app.get("/authors/")
async def get_author_by_name(first_name:str|None =None, last_name:str|None=None) -> list[AuthorModel]:
    result_list = []
    for author in db_authors:
        if first_name != None and first_name.lower() in author["first_name"].lower():
            result_list.append(author)
        if last_name != None and last_name.lower() in author["last_name"].lower():
            if author not in result_list:
                result_list.append(author)
    if len(result_list) == 0:
        raise HTTPException(status_code=404, detail=f"Name {first_name if first_name != None else last_name} not found")
    return result_list


@app.post("/authors/")
async def create_Author(author:AuthorModelIn) -> AuthorModel:
    new_author = AuthorModel(
        author_id=len(db_authors)+1,
        first_name=author.first_name,
        last_name=author.last_name,
        books=author.books,
        rate = author.rate
    )

    db_authors.append(new_author)
    
    return new_author

@app.put("/authors/{id}")
async def update_author(id:int, author_input:AuthorModelUpdate) -> AuthorModel:
    for author in db_authors:
        if author["author_id"] == id:
            author["rate"] = author_input.rate
            if len(author_input.books)!=0:
                author["books"] = author["books"] + author_input.books
            return author
    raise HTTPException(status_code=404, detail="Author not found")

@app.delete("/authors/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(id:int):
    for index,author in enumerate(db_authors):
        if author["author_id"] == id:
            del db_authors[index]
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail="Author not found")

                 

    
        

    