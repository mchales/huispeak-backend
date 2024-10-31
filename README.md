# Huispeak Backend

**Huispeak** is a Django-based backend designed for a web application that aids Chinese language learners in practicing conversation with an emphasis on Chinese cultural elements and practical, real-life scenarios.

## Features

- **User Authentication**: Secure user login, registration, and account management, implemented with Simple JWT and Djoser for robust JWT-based authentication.
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

## Running the Server

To start the development server, run:

```bash
python manage.py runserver
```

## Running Tests

Tests are managed with `pytest`. To run all tests, use:

```bash
pytest
```
