# Simple Frontend - Quick Start Guide

## ✅ Setup Complete!

Your AutoQ system is now running with a **simple HTML/CSS frontend** (no login required).

## 🚀 Access the Application

Open your browser and go to:
**http://localhost:3001**

## 🎯 How It Works

The frontend automatically logs in with a default user in the background, so you can use all features without manual login.

- **Username:** default
- **Password:** default123
- **Auto-login:** Happens automatically when you open the page

## 📋 Features Available

### 1. **Upload Documents**
- Drag & drop PDF files
- Or click to browse and select
- Automatic processing with AI/ML

### 2. **Generate Questions**
- Select processed document
- Choose number of questions
- Select question types (MCQ, True/False, Short Answer, Long Answer)
- AI generates questions using NLP and Machine Learning

### 3. **Create Question Papers**
- Enter paper title
- Set total marks and duration
- System creates formatted question paper
- Download as PDF

## 🔧 Running the Servers

### Backend (Port 8000)
```bash
cd c:\Users\karis\OneDrive\Desktop\A20\CascadeProjects\AutoQ
start_backend.bat
```

### Frontend (Port 3001)
```bash
cd c:\Users\karis\OneDrive\Desktop\A20\CascadeProjects\AutoQ\simple-frontend
python -m http.server 3001
```

## 🛠️ Technology Stack

### Frontend
- **HTML5** - Structure
- **CSS3** - Beautiful gradient design with animations
- **JavaScript** - Dynamic functionality
- **Fetch API** - Communication with backend

### Backend (Machine Learning)
- **FastAPI** - REST API framework
- **spaCy** - NLP for text processing
- **Transformers** - AI models for question generation
- **PyPDF2** - PDF text extraction
- **SQLite** - Database

## 📊 Machine Learning Features

1. **Text Extraction** - Extracts content from PDFs
2. **Topic Detection** - Identifies key topics using NLP
3. **Question Generation** - Uses AI models to create questions
4. **Difficulty Classification** - Categorizes questions by difficulty
5. **Answer Generation** - Creates correct answers and explanations

## 🎨 UI Features

- **Gradient Background** - Modern purple gradient
- **Smooth Animations** - Fade-in and slide-up effects
- **Responsive Design** - Works on all screen sizes
- **Loading Indicators** - Shows AI processing status
- **Drag & Drop** - Easy file upload
- **Clean Cards** - Organized content sections

## 📝 Workflow

1. **Upload PDF** → System extracts text
2. **Process Document** → AI analyzes content and detects topics
3. **Generate Questions** → ML models create questions
4. **Create Paper** → Compile questions into formatted paper
5. **Download** → Get PDF of question paper

## 🔍 API Endpoints Used

- `POST /api/v1/documents/upload` - Upload PDF
- `POST /api/v1/documents/{id}/process` - Process document
- `GET /api/v1/documents/` - List documents
- `POST /api/v1/questions/generate` - Generate questions with AI
- `POST /api/v1/papers/create` - Create question paper
- `GET /api/v1/papers/{id}/export` - Download PDF

## 💡 Tips

- Use **text-based PDFs** (not scanned images) for best results
- **Process documents** before generating questions
- The AI works better with **well-formatted educational content**
- You can generate **multiple question sets** from the same document
- **Adjust difficulty distribution** for different exam levels

## 🐛 Troubleshooting

### Upload fails
- Check if backend is running on port 8000
- Ensure PDF is not corrupted
- File size should be under 50MB

### Questions not generating
- Make sure document is processed first
- Check if document has sufficient text content
- Try with a different PDF

### Page not loading
- Verify frontend server is running on port 3001
- Check browser console for errors
- Try clearing browser cache

## 🎓 Example Use Case

1. Upload a computer science textbook chapter (PDF)
2. System processes and extracts 50 pages of content
3. Generate 20 questions (mix of MCQ and short answer)
4. Create exam paper with 100 marks, 60 minutes duration
5. Download professional PDF with institution header

---

**Enjoy using AutoQ! 🎉**

For the original React frontend with full authentication, use port 3000.
For this simple no-login version, use port 3001.
