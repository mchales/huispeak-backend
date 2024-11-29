# Huispeak Backend

**Huispeak** is a Django-based backend designed for a web application that aids Chinese language learners in practicing conversation with an emphasis on Chinese cultural elements and practical, real-life scenarios.

## Features

- **User Authentication**: Secure user login, registration, and account management, implemented with Simple JWT and Djoser for JWT-based authentication.
- **Lesson Creation**: Create and manage conversational lessons for immersive learning.
- **OpenAI Assistant Integration**: Enhance conversation practice with AI-generated responses and guidance.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/huispeak-backend.git
   cd huispeak-backend
   ```

2. **Install dependencies**:
   ```bash
   pip install -r development/requirements.txt
   ```
3. **Database Setup**
   If you don't want to configure PostgreSQL with a tool like pgAdmin, you should use the sqlite database as your main database. Within settings.py include
   ```python
   if ENVIRONMENT == 'development':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
   ```

## Running the Server

To start the development server, run:

```bash
python manage.py runserver
```
You can access the server at http://127.0.0.1:8000/ and create a user to log in with the command
```bash
python manage.py createsuperuser
```

## Running Tests

Tests are managed with `pytest`. To run all tests, use:

```bash
pytest
```
