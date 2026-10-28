# HOME LIBRARY FASTAPI

A REST API built with Python, FastAPI and SQLModel as a personal learning project.

The goal is to build an application for managing my home library by tracking books, recording reading progress, and keeping information about books and their authors in one place

The project is being developed gradually  as I learn backend, database integration, and API design.

## Current Features

Create, retrieve, update, and delete books.
Create, retrieve, update, and delete authors.
Retrieve a book or author by ID.
Retrieve lists of books and authors.
Associate books with authors using database relationships.
Track reading status: unread, reading, or read.
Store an optional rating from 0 to 5 and a written review for each book.
Support partial updates using HTTP PATCH.
Validate request data using SQLModel and Pydantic.
Handle missing books and authors with HTTP 404 responses.
Persist data in a SQLite database.
Expose interactive API documentation through FastAPI.

## Technologies
Python
FastAPI
SQLModel
SQLite
Pydantic
uv for project and dependency management

### Prerequisites
Python
uv 

### Installation

Step-by-step instructions to get a local development environment running:

1. Clone the repository
   git clone 
   
2. Install project dependencies
   uv sync

3. Start the project
    uv run fastapi dev


Data Model

Book:

Name
Reading status
Optional rating
Optional review
Optional author ID

Author:
First name
Last name

Books and authors are stored as separate database records. A foreign key connects each book to its author, while SQLModel relationships allow navigation between an author and their books.


## Current Limitations

The API does not yet implement book search or filtering.
Each book can be associated with at most one author.
Authentication and authorization are not implemented.
Automated tests are not yet implemented.
Database schema migrations are not yet configured.
Author deletion behavior when books reference that author still needs to be explicitly defined and tested.


## Planned Improvements

Add automated tests for API endpoints.
Implement search and filtering by book name and author.
Define and test deletion behavior for related books and authors.
Improve database relationship handling and validation.
Add a wishlist for books I want to buy.
Explore database migrations as the schema evolves.
Improve project structure and error handling..


## Learning Goals

Through this project, I am practising REST API design, CRUD operations, request validation, HTTP status codes, and Python application structure.

As I learn more about backend development and databases, I plan to refactor the project and improve its design.