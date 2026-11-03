Productivity App – Flask Backend
Project Description

This project is a secure Flask REST API for a productivity application that allows users to register, log in, and manage their personal notes.

The application uses JWT authentication to protect routes and ensures that users can only access, update, and delete their own notes.

Technologies Used
Python
Flask
Flask-SQLAlchemy
Flask-JWT-Extended
SQLite
Flask-CORS
Werkzeug Password Hashing
Pytest
Pipenv
Installation Instructions
Clone the repository:
bash
git clone YOUR_GITHUB_REPOSITORY_URL

Navigate into the server directory:
bash
cd server

Install dependencies:
bash
pipenv install

Activate the virtual environment:
bash
pipenv shell

Create the database:
bash
python -c "from app import create_app; from models import db; app=create_app(); app.app_context().push(); db.create_all()"

Seed the database:
bash
python seed.py

Running the Application

Start the Flask development server:

bash
python app.py


The API will run at:

http://127.0.0.1:5000

API Endpoints
Authentication
Method	Endpoint	Description
POST	/signup	Register a new user
POST	/login	Authenticate an existing user
GET	/me	Retrieve the authenticated user's information
Notes

All notes endpoints require a valid JWT access token in the Authorization header.

Method	Endpoint	Description
POST	/notes	Create a new note
GET	/notes	Retrieve the authenticated user's notes
PATCH	/notes/<id>	Update an existing note
PUT	/notes/<id>	Replace or update a note
DELETE	/notes/<id>	Delete a note
Pagination

The notes endpoint supports pagination using query parameters.

Example:

text
GET /notes?page=1&per_page=10

page: The page number.
per_page: Number of notes displayed per page.
Security Features
Passwords are securely hashed before being stored.
JWT authentication protects private routes.
Users can only access their own notes.
Unauthorized requests are rejected.
Duplicate usernames are prevented.
Input validation is implemented for registration and note creation.
Database Models
User
id
username
password_hash
Note
id
title
content
user_id

Each note belongs to a specific user through a foreign key relationship.

Testing

Run the automated test suite:

bash
pipenv run pytest -v


The tests cover authentication, note CRUD operations, authorization, and pagination.

Sample Login Credentials

After running the seed file:

Username: katelyn

Password: password123

Username: testuser

Password: password123

Author

Katelyn