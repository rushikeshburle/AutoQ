# AutoQ API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication

All endpoints (except `/auth/register` and `/auth/login`) require JWT authentication.

Include the token in the Authorization header:
```
Authorization: Bearer <your_token>
```

## Endpoints

### Authentication

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "password123",
  "full_name": "John Doe",
  "role": "instructor"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "John Doe",
  "role": "instructor",
  "is_active": true
}
```

#### Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=username&password=password123
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### Get Current User
```http
GET /auth/me
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "John Doe",
  "role": "instructor",
  "is_active": true
}
```

### Documents

#### Upload Document
```http
POST /documents/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <pdf_file>
```

**Response:**
```json
{
  "id": 1,
  "filename": "uuid-filename.pdf",
  "original_filename": "lecture_notes.pdf",
  "file_size": 1024000,
  "is_processed": false,
  "processing_status": "pending",
  "created_at": "2024-01-01T00:00:00"
}
```

#### Process Document
```http
POST /documents/{document_id}/process
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Document processed successfully",
  "document_id": 1,
  "topics_found": 5
}
```

#### List Documents
```http
GET /documents/
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": 1,
    "filename": "uuid-filename.pdf",
    "original_filename": "lecture_notes.pdf",
    "file_size": 1024000,
    "is_processed": true,
    "processing_status": "completed",
    "created_at": "2024-01-01T00:00:00"
  }
]
```

#### Get Document Details
```http
GET /documents/{document_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "filename": "uuid-filename.pdf",
  "original_filename": "lecture_notes.pdf",
  "file_size": 1024000,
  "is_processed": true,
  "processing_status": "completed",
  "created_at": "2024-01-01T00:00:00",
  "extracted_text": "Full text content...",
  "topics": [
    {
      "id": 1,
      "name": "Introduction",
      "description": "Topic description..."
    }
  ]
}
```

#### Delete Document
```http
DELETE /documents/{document_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Document deleted successfully"
}
```

### Questions

#### Generate Questions
```http
POST /questions/generate
Authorization: Bearer <token>
Content-Type: application/json

{
  "document_id": 1,
  "num_questions": 10,
  "question_types": ["mcq", "short_answer"],
  "difficulty_easy": 0.4,
  "difficulty_medium": 0.4,
  "difficulty_hard": 0.2,
  "topic_ids": [1, 2]
}
```

**Response:**
```json
[
  {
    "id": 1,
    "question_text": "What is Python?",
    "question_type": "mcq",
    "difficulty": "easy",
    "option_a": "A programming language",
    "option_b": "A snake",
    "option_c": "A framework",
    "option_d": "A library",
    "correct_answer": "A programming language",
    "explanation": "Python is a high-level programming language.",
    "suggested_marks": 1.0,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

#### List Questions
```http
GET /questions/?question_type=mcq&difficulty=easy&document_id=1
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": 1,
    "question_text": "What is Python?",
    "question_type": "mcq",
    "difficulty": "easy",
    "correct_answer": "A programming language",
    "suggested_marks": 1.0,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

#### Create Question
```http
POST /questions/
Authorization: Bearer <token>
Content-Type: application/json

{
  "question_text": "What is Python?",
  "question_type": "mcq",
  "difficulty": "easy",
  "option_a": "A programming language",
  "option_b": "A snake",
  "option_c": "A framework",
  "option_d": "A library",
  "correct_answer": "A programming language",
  "explanation": "Python is a high-level programming language.",
  "suggested_marks": 1.0,
  "source_document_id": 1
}
```

#### Update Question
```http
PUT /questions/{question_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "question_text": "Updated question text",
  "difficulty": "medium"
}
```

#### Delete Question
```http
DELETE /questions/{question_id}
Authorization: Bearer <token>
```

### Question Papers

#### Create Question Paper
```http
POST /papers/
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Mid-term Exam 2024",
  "description": "Computer Science Mid-term",
  "question_ids": [1, 2, 3, 4, 5],
  "total_marks": 100,
  "duration_minutes": 60,
  "instructions": "Read all questions carefully.",
  "institution_name": "ABC University"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Mid-term Exam 2024",
  "description": "Computer Science Mid-term",
  "total_marks": 100,
  "duration_minutes": 60,
  "is_published": false,
  "created_at": "2024-01-01T00:00:00"
}
```

#### List Question Papers
```http
GET /papers/
Authorization: Bearer <token>
```

#### Get Question Paper
```http
GET /papers/{paper_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "title": "Mid-term Exam 2024",
  "description": "Computer Science Mid-term",
  "total_marks": 100,
  "duration_minutes": 60,
  "is_published": false,
  "created_at": "2024-01-01T00:00:00",
  "questions": [
    {
      "id": 1,
      "question_text": "What is Python?",
      "question_type": "mcq",
      "difficulty": "easy",
      "suggested_marks": 1.0
    }
  ]
}
```

#### Export Question Paper
```http
POST /papers/{paper_id}/export
Authorization: Bearer <token>
Content-Type: application/json

{
  "format": "pdf",
  "include_answers": false
}
```

**Response:** Binary file download (PDF or DOCX)

#### Publish Question Paper
```http
POST /papers/{paper_id}/publish
Authorization: Bearer <token>
```

#### Update Question Paper
```http
PUT /papers/{paper_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Updated Title",
  "total_marks": 120
}
```

#### Delete Question Paper
```http
DELETE /papers/{paper_id}
Authorization: Bearer <token>
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

Currently no rate limiting is implemented. For production, consider implementing rate limiting based on your requirements.

## Interactive Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

Visit `http://localhost:8000/redoc` for ReDoc documentation.
