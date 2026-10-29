from fastapi import FastAPI
from .database import create_db_and_tables
from .routers import books, authors


# def get_session():
#     with Session(engine) as session:
#         yield session

# SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

app.include_router(books.router)
app.include_router(authors.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()




    