# AutoQ — Automatic Question Paper Generator

**Generate reliable, balanced question papers from your PDFs — instantly. Teach. Assess. Iterate.**

AutoQ is a Python web application that transforms instructor-provided PDFs (lecture notes, slides, textbooks, syllabus) into polished, printable question papers and student practice sets — automatically, intelligently, and at scale.

## 🎯 Key Features

- **One-click paper generation**: Upload a PDF, choose preferences, download formatted question paper
- **Multiple question formats**: MCQ, True/False, Short Answer, Long Answer, Code/Programming, Fill-in-the-blanks
- **Automatic difficulty scaling**: Generate mixed, easy-only, or progressively harder question sets
- **Solutions & answer key**: Model answers and scoring suggestions included
- **Topic-aware generation**: Questions grouped by chapter/topic
- **Custom templates & branding**: Printable layouts with institution header/footer
- **Student practice mode**: Randomized practice quizzes with instant feedback
- **Question bank & reuse**: Store, tag, and reuse questions across semesters
- **Plagiarism & duplication check**: Avoid repeated questions across papers
- **Privacy & security**: Secure PDF processing with encryption options

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+ (for frontend)
- PostgreSQL (or SQLite for development)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Docker Setup (Recommended)

```bash
docker-compose up --build
```

Access the application at `http://localhost:3000`

## 📁 Project Structure

```
AutoQ/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   │   ├── pdf_processor.py
│   │   │   ├── question_generator.py
│   │   │   ├── export_service.py
│   │   │   └── nlp_engine.py
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.tsx
│   └── package.json
├── docker-compose.yml
└── README.md
```

## 🛠️ Tech Stack

**Backend:**
- FastAPI (Python web framework)
- spaCy + transformers (NLP & question generation)
- PyMuPDF (PDF text extraction)
- PostgreSQL (database)
- ReportLab (PDF export)
- python-docx (Word export)

**Frontend:**
- React + TypeScript
- TailwindCSS (styling)
- shadcn/ui (components)
- Lucide React (icons)
- Axios (API calls)

## 📖 Usage

1. **Upload PDF**: Click "Upload PDF" and select your lecture notes or textbook
2. **Configure**: Choose question types, number, difficulty mix, and template
3. **Generate**: AI processes the PDF and creates questions with answers
4. **Review**: Preview and edit questions in the browser
5. **Export**: Download as PDF/Word or publish as practice quiz

## 🔒 Security

- Uploaded PDFs are encrypted at rest
- Optional local-only processing mode
- JWT-based authentication
- Role-based access control (Admin, Instructor, Student)

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please read CONTRIBUTING.md for guidelines.

## 📧 Support

For issues and questions, please open a GitHub issue or contact support@autoq.edu
