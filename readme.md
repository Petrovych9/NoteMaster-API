# Note Master API

> A FastAPI-based RESTful API for managing text notes. Basic CRUD operations using FastAPI, database integration, and user authentication.


The NoteMaster-API project provides a platform for users to manage text notes with various features, including:

- User Registration and Authentication using JWT (JSON Web Tokens).
- Note Management: Create, read, update, and delete text notes with titles and content.
- Note Categories: Categorize notes (e.g., personal, work, ideas).
- Additional Features: Text search, sorting by date, and archiving/favoriting notes.

## Technologies Used

The project is built using the following technologies:

- **FastAPI**: A modern Python web framework for building APIs.
- **Python**: The primary programming language for backend logic.
- **SQLAlchemy**: Used for database management and ORM (Object-Relational Mapping).
- **JSON Web Tokens (JWT)**: Used for secure user authentication.
- **Pydantic**: Used for data validation and serialization.
- **Uvicorn**: ASGI server for running the FastAPI application.
- **Databases**: An asynchronous database library for database interaction (supports various databases like SQLite, PostgreSQL, etc.).

## Key Features

### User Registration and Authentication

- Users can register and securely log in using JWT-based authentication.

### Note Management

- Create, read, update, and delete text notes.
- Each note consists of a title and content.

### Note Categories

- Organize notes by categorizing them into predefined categories (e.g., personal, work, ideas).

### Additional Features

- Basic text search functionality for notes.
- Sort notes by date created or modified.
- Archive or "favorite" notes for easy access.



# Getting Started
### 1. Clone the repository

   ```sh
   cd folder-to-save
  ``` 
   ```
   git clone git@github.com:Petrovych9/NoteMaster-API.git
   ```
### 2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   ```

### 3. Install project dependencies:
   ```
   pip install -r requirements.txt
   ```
### 4. Initialize the database and create tables:
   ```
   python -m alembic upgrade head
   ```
### 5. Start the development server:
   ```
   uvicorn main:app --reload
   ```


# API Endpoints

| Endpoint                | GET     | POST    | PUT     | DELETE  |
|-------------------------|---------|---------|---------|---------|
| /users/register         |         |   Register a new user   |         |         |
| /users/login            |         |   Log in and obtain an access token  |         |         |
| /notes/                 |   Retrieve all notes    |   Create a new note   |       |       |
| /notes/{note_id}/       |   Retrieve a specific note by ID   |         |   Update a specific note by ID    |   Delete a specific note by ID   |



 - For detailed documentation, visit the Swagger UI at http://localhost:8000/docs.



## Contact
[GitHub - Petrovych9](https://github.com/Petrovych9)

### Other projects

- current - [Note Master API](https://github.com/Petrovych9/NoteMaster-API)
- [Mini Masterworks](https://github.com/Petrovych9/Mini-Masterworks)
- [Food Club](https://github.com/Petrovych9/Food-Club)
- [Training Club]()
