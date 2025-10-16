# AutoQ Quick Start Guide

Get AutoQ running in 5 minutes!

## Prerequisites

- Docker and Docker Compose installed
- OR Python 3.9+ and Node.js 16+

## Option 1: Docker (Fastest)

```bash
# 1. Navigate to AutoQ directory
cd AutoQ

# 2. Create environment file
cp backend/.env.example backend/.env

# 3. Start all services
docker-compose up -d

# 4. Wait for services to start (about 30 seconds)
# Check status: docker-compose ps

# 5. Open your browser
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

That's it! AutoQ is now running.

## Option 2: Manual Setup

### Backend

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Download NLP model
python -m spacy download en_core_web_sm

# 6. Create environment file
cp .env.example .env

# 7. Run backend
uvicorn app.main:app --reload
```

Backend is now running at http://localhost:8000

### Frontend

Open a new terminal:

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Run frontend
npm run dev
```

Frontend is now running at http://localhost:3000

## First Steps

### 1. Create an Account

1. Go to http://localhost:3000/register
2. Fill in your details
3. Select "Instructor" role
4. Click Register

### 2. Login

1. Go to http://localhost:3000/login
2. Enter your credentials
3. Click Login

### 3. Upload a PDF

1. Click "Documents" in the sidebar
2. Click the upload area
3. Select a PDF file (lecture notes, textbook, etc.)
4. Click "Upload"
5. Click "Process" button on the uploaded document
6. Wait for processing to complete

### 4. Generate Questions

1. Click "Questions" in the sidebar
2. Click "Generate Questions"
3. Select your processed document
4. Adjust settings:
   - Number of questions: 10
   - Question types: MCQ, Short Answer
   - Difficulty: Easy 40%, Medium 40%, Hard 20%
5. Click "Generate"
6. Wait for questions to be generated

### 5. Create Question Paper

1. Click "Question Papers" in the sidebar
2. Click "Create Paper"
3. Fill in paper details:
   - Title: "Sample Exam"
   - Total Marks: 100
   - Duration: 60 minutes
4. Select questions by clicking on them
5. Click "Create Paper"

### 6. Export Question Paper

1. Find your paper in the list
2. Click the download icon
3. Choose format (PDF or Word)
4. Choose whether to include answers
5. File will download automatically

## Tips

- **Use quality PDFs**: Better formatted PDFs produce better questions
- **Process first**: Always process documents before generating questions
- **Review questions**: Edit generated questions to improve quality
- **Save papers**: Create multiple versions for different classes
- **Export with answers**: Great for creating answer keys

## Common Issues

### "Document processing failed"
- Check if PDF is text-based (not scanned images)
- Try a different PDF

### "No questions generated"
- Ensure document is processed
- Check if document has sufficient text content
- Try increasing number of questions

### "Cannot connect to backend"
- Ensure backend is running on port 8000
- Check if any firewall is blocking

### "Page not loading"
- Clear browser cache
- Try a different browser
- Check console for errors

## Next Steps

- Read the full [README.md](README.md) for detailed information
- Check [SETUP.md](SETUP.md) for advanced configuration
- Review [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API details
- Explore [FEATURES.md](FEATURES.md) for all features

## Need Help?

- Check the documentation
- Open an issue on GitHub
- Review API docs at http://localhost:8000/docs

## Stop Services

### Docker
```bash
docker-compose down
```

### Manual
Press `Ctrl+C` in both terminal windows

---

**Congratulations!** You're now ready to use AutoQ to generate question papers automatically. 🎉
