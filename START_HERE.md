# 🚀 START HERE - AutoQ Quick Setup

Welcome to **AutoQ** - Your Automatic Question Paper Generator!

## ⚡ Fastest Way to Get Started

### Option 1: Docker (Recommended - 2 Minutes)

```bash
# 1. Open terminal in AutoQ folder
cd AutoQ

# 2. Copy environment file
cp backend/.env.example backend/.env

# 3. Start everything
docker-compose up -d

# 4. Open browser
# Go to: http://localhost:3000
```

**That's it!** AutoQ is now running. 🎉

### Option 2: Manual Setup (5 Minutes)

**Terminal 1 - Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
# OR
source venv/bin/activate       # Mac/Linux

pip install -r requirements.txt
python -m spacy download en_core_web_sm
cp .env.example .env
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Open:** http://localhost:3000

---

## 📖 What to Read Next

### First Time Users
1. **[QUICKSTART.md](QUICKSTART.md)** - Step-by-step first usage guide
2. **[README.md](README.md)** - Complete overview and features

### Developers
1. **[SETUP.md](SETUP.md)** - Detailed setup and configuration
2. **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Code organization
3. **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - API reference

### Deployment
1. **[RUN_INSTRUCTIONS.md](RUN_INSTRUCTIONS.md)** - Running the app
2. **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment

### Reference
1. **[FEATURES.md](FEATURES.md)** - All features explained
2. **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute
3. **[SUMMARY.md](SUMMARY.md)** - Project overview

---

## 🎯 Quick Usage Flow

1. **Register** → Create an account at `/register`
2. **Upload** → Upload a PDF document
3. **Process** → Click "Process" on uploaded document
4. **Generate** → Generate questions from processed document
5. **Create** → Create a question paper from generated questions
6. **Export** → Download as PDF or Word

---

## 🆘 Need Help?

### Common Issues

**"Backend won't start"**
- Check Python version: `python --version` (need 3.9+)
- Install dependencies: `pip install -r requirements.txt`

**"Frontend won't start"**
- Check Node version: `node --version` (need 16+)
- Clear and reinstall: `rm -rf node_modules && npm install`

**"spaCy model error"**
- Run: `python -m spacy download en_core_web_sm`

**"Port already in use"**
- Backend uses port 8000
- Frontend uses port 3000
- Check if something else is using these ports

### Get More Help
- Check **[QUICKSTART.md](QUICKSTART.md)** for detailed troubleshooting
- Visit API docs: http://localhost:8000/docs
- Review error messages in terminal

---

## ✨ Key Features

- 📄 **PDF Upload** - Upload any educational PDF
- 🤖 **AI Generation** - Automatic question generation
- 📝 **6 Question Types** - MCQ, True/False, Short, Long, Fill-blank, Programming
- 📊 **3 Difficulty Levels** - Easy, Medium, Hard
- 📑 **Professional Export** - PDF and Word formats
- 🔐 **Secure** - JWT authentication
- 🎨 **Modern UI** - Beautiful, responsive interface

---

## 📦 What's Included

```
AutoQ/
├── backend/          # FastAPI Python backend
├── frontend/         # React TypeScript frontend
├── docker-compose.yml
└── Documentation (12+ markdown files)
```

---

## 🎓 System Requirements

**Minimum:**
- Python 3.9+
- Node.js 16+
- 4GB RAM
- 10GB storage

**Recommended:**
- Python 3.11+
- Node.js 18+
- 8GB RAM
- 50GB storage

---

## 🌟 Quick Tips

💡 **Use quality PDFs** - Text-based PDFs work best (not scanned images)

💡 **Process first** - Always process documents before generating questions

💡 **Review questions** - Edit generated questions to improve quality

💡 **Save papers** - Create multiple versions for different classes

💡 **Export with answers** - Great for creating answer keys

---

## 🎉 You're Ready!

Choose your setup method above and get started in minutes.

For detailed information, check out **[QUICKSTART.md](QUICKSTART.md)**.

**Happy Teaching! 📚**

---

**AutoQ** - Transform your PDFs into question papers instantly.
