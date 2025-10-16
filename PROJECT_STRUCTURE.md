# AutoQ Project Structure

```
AutoQ/
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── api/                     # API endpoints
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py         # Authentication endpoints
│   │   │   │   ├── documents.py    # Document management
│   │   │   │   ├── questions.py    # Question management
│   │   │   │   └── papers.py       # Question paper endpoints
│   │   │   └── __init__.py
│   │   ├── core/                    # Core configuration
│   │   │   ├── __init__.py
│   │   │   ├── config.py           # Application settings
│   │   │   └── security.py         # Security utilities
│   │   ├── models/                  # Database models
│   │   │   ├── __init__.py
│   │   │   ├── database.py         # Database connection
│   │   │   ├── user.py             # User model
│   │   │   ├── document.py         # Document model
│   │   │   ├── question.py         # Question model
│   │   │   └── question_paper.py   # Question paper model
│   │   ├── services/                # Business logic
│   │   │   ├── __init__.py
│   │   │   ├── pdf_processor.py    # PDF text extraction
│   │   │   ├── nlp_engine.py       # NLP processing
│   │   │   ├── question_generator.py # Question generation
│   │   │   └── export_service.py   # PDF/Word export
│   │   ├── __init__.py
│   │   └── main.py                  # FastAPI application
│   ├── tests/                       # Backend tests
│   │   ├── __init__.py
│   │   └── test_api.py
│   ├── uploads/                     # Uploaded PDFs (gitignored)
│   ├── exports/                     # Exported papers (gitignored)
│   ├── .env.example                 # Environment template
│   ├── .env                         # Environment variables (gitignored)
│   ├── Dockerfile                   # Docker configuration
│   ├── pytest.ini                   # Pytest configuration
│   └── requirements.txt             # Python dependencies
│
├── frontend/                         # React Frontend
│   ├── src/
│   │   ├── components/              # Reusable components
│   │   │   └── Layout.tsx          # Main layout component
│   │   ├── pages/                   # Page components
│   │   │   ├── Login.tsx           # Login page
│   │   │   ├── Register.tsx        # Registration page
│   │   │   ├── Dashboard.tsx       # Dashboard
│   │   │   ├── Documents.tsx       # Document management
│   │   │   ├── Questions.tsx       # Question management
│   │   │   ├── QuestionPapers.tsx  # Paper listing
│   │   │   └── CreatePaper.tsx     # Paper creation
│   │   ├── services/                # API services
│   │   │   └── api.ts              # API client
│   │   ├── store/                   # State management
│   │   │   └── authStore.ts        # Auth state (Zustand)
│   │   ├── App.tsx                  # Main app component
│   │   ├── main.tsx                 # Entry point
│   │   └── index.css                # Global styles
│   ├── public/                      # Static assets
│   ├── .env.example                 # Environment template
│   ├── Dockerfile                   # Docker configuration
│   ├── index.html                   # HTML template
│   ├── package.json                 # Node dependencies
│   ├── tailwind.config.js           # TailwindCSS config
│   ├── tsconfig.json                # TypeScript config
│   └── vite.config.ts               # Vite config
│
├── .gitignore                        # Git ignore rules
├── docker-compose.yml                # Docker Compose config
├── LICENSE                           # MIT License
├── README.md                         # Main documentation
├── SETUP.md                          # Setup instructions
├── QUICKSTART.md                     # Quick start guide
├── FEATURES.md                       # Feature documentation
├── API_DOCUMENTATION.md              # API reference
├── CONTRIBUTING.md                   # Contribution guidelines
├── CHANGELOG.md                      # Version history
└── PROJECT_STRUCTURE.md              # This file
```

## Key Directories

### Backend (`/backend`)

**`app/api/v1/`** - REST API endpoints organized by resource
- `auth.py` - User registration, login, token management
- `documents.py` - PDF upload, processing, listing
- `questions.py` - Question generation, CRUD operations
- `papers.py` - Question paper creation and export

**`app/core/`** - Core application configuration
- `config.py` - Settings loaded from environment variables
- `security.py` - JWT authentication, password hashing

**`app/models/`** - SQLAlchemy database models
- `database.py` - Database connection and session management
- `user.py` - User model with roles
- `document.py` - Document metadata and processing status
- `question.py` - Question model with types and difficulty
- `question_paper.py` - Question paper configuration

**`app/services/`** - Business logic layer
- `pdf_processor.py` - Extract text from PDFs, detect sections
- `nlp_engine.py` - NLP analysis using spaCy
- `question_generator.py` - Generate questions from text
- `export_service.py` - Export to PDF/Word formats

### Frontend (`/frontend`)

**`src/pages/`** - Main application pages
- `Login.tsx` - User authentication
- `Dashboard.tsx` - Overview and statistics
- `Documents.tsx` - Upload and manage PDFs
- `Questions.tsx` - View and generate questions
- `QuestionPapers.tsx` - List all papers
- `CreatePaper.tsx` - Create new paper

**`src/components/`** - Reusable UI components
- `Layout.tsx` - Main layout with navigation

**`src/services/`** - API integration
- `api.ts` - Axios client with interceptors

**`src/store/`** - Global state management
- `authStore.ts` - Authentication state using Zustand

## Technology Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Database**: SQLAlchemy with PostgreSQL/SQLite
- **Authentication**: JWT with python-jose
- **PDF Processing**: PyMuPDF (fitz)
- **NLP**: spaCy 3.7+
- **Export**: ReportLab (PDF), python-docx (Word)

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite 5
- **Styling**: TailwindCSS 3.3
- **State**: Zustand 4
- **HTTP Client**: Axios 1.6
- **Icons**: Lucide React
- **Routing**: React Router 6

### DevOps
- **Containerization**: Docker & Docker Compose
- **Database**: PostgreSQL 15 (production), SQLite (dev)
- **Cache**: Redis 7 (optional, for Celery)

## Data Flow

1. **Document Upload**
   ```
   User → Frontend → API → Storage → Database
   ```

2. **Document Processing**
   ```
   API → PDF Processor → NLP Engine → Database (topics)
   ```

3. **Question Generation**
   ```
   API → NLP Engine → Question Generator → Database (questions)
   ```

4. **Paper Creation**
   ```
   Frontend → API → Database (paper + question links)
   ```

5. **Paper Export**
   ```
   API → Export Service → PDF/Word file → Download
   ```

## Database Schema

### Users
- id, email, username, hashed_password, full_name, role, is_active

### Documents
- id, filename, file_path, file_size, extracted_text, is_processed, owner_id

### Topics
- id, name, description, document_id

### Questions
- id, question_text, question_type, difficulty, options, correct_answer, explanation, suggested_marks, topic_id, creator_id

### Question Papers
- id, title, description, total_marks, duration_minutes, instructions, creator_id

### Question-Paper Association (Many-to-Many)
- question_paper_id, question_id, order, marks

## Configuration Files

- **`.env`** - Environment variables (secrets, database URL)
- **`docker-compose.yml`** - Multi-container Docker setup
- **`requirements.txt`** - Python dependencies
- **`package.json`** - Node.js dependencies
- **`tailwind.config.js`** - TailwindCSS customization
- **`tsconfig.json`** - TypeScript compiler options

## Development Workflow

1. **Backend Development**
   ```bash
   cd backend
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   uvicorn app.main:app --reload
   ```

2. **Frontend Development**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Running Tests**
   ```bash
   cd backend
   pytest
   ```

4. **Docker Development**
   ```bash
   docker-compose up --build
   ```

## API Versioning

Current version: **v1**

All API endpoints are prefixed with `/api/v1/`

Future versions will use `/api/v2/`, etc., maintaining backward compatibility.

## Security Considerations

- Passwords hashed with bcrypt
- JWT tokens for authentication
- CORS configured for allowed origins
- File upload size limits enforced
- SQL injection prevented by ORM
- XSS protection in frontend
- HTTPS recommended for production

## Scalability

- Stateless API design
- Database connection pooling
- Async/await for I/O operations
- Horizontal scaling possible
- Redis for caching (optional)
- Celery for background tasks (optional)

## Monitoring

- Health check endpoint: `/health`
- API documentation: `/docs`
- Logs in console (configurable)
- Database query logging (dev mode)
