# HOME LIBRARY FASTAPI

A REST API built with Python and FastAPI as a personal learning project.

The goal is to develop application for managing my home books by tracking the books I have read, and keeping information about books and authors in one place.

The project is being developed gradually  as I learn backend.

## Current Features

Retrieve all books and retrieve a book by ID
Search books by title
Search books by author's first or last name
Add new books to the collection
Update a book's reading status, rating, and review
Delete books from the collection
Validate request data using Pydantic models
Restrict reading status to read or unread
Handle errors using HTTP status codes

## Technologies
Python
FastAPI
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

## Current Limitations

Book and author information is stored together in a book entry; authors are not managed as separate resources.
Each book entry has one current reading status, rating, and review.
The project does not yet use a database or automated tests.


## Planned Improvements

Database for persistent storage.
Improve the relationship between books and authors.
Add a wishlist for books I want to buy.
Improve input validation and search behaviour.
Add automated tests for API endpoints.


## Learning Goals

Through this project, I am practising REST API design, CRUD operations, request validation, HTTP status codes, and Python application structure.

As I learn more about backend development and databases, I plan to refactor the project and improve its design.