# HOME LIBRARY FASTAPI

A REST API built with Python and FastAPI as a personal learning project.4

The goal is to develop application for managing my home book, by tracking the book I have read, and keeping information about books and authors in one place.

The project is being developed gradually  as I learn backend.

## Current Features

Create, retrieve, update, and delete authors
Search authors by first name and last name
Store information about authors and their books
Validate request data using Pydantic models
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

Data is stored in an in-memory list and is lost when the application restarts.
Books are currently stored as information associated with authors rather than as separate list/datatable.


## Planned Improvements

Make books the main resource of the API
Add the ability to track read and unread books
Improve the relationship between books and authors
Add a wishlist for books I want to buy
Introduce a database for storage


## Learning Goals

Through this project, I am practising REST API design, CRUD operations, request validation, HTTP status codes, and Python application structure.

As I learn more about backend development and databases, I plan to refactor the project and improve its design.