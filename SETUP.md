# AutoQ Setup Guide

## Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- PostgreSQL (optional, SQLite works for development)
- Docker and Docker Compose (optional, for containerized setup)

## Option 1: Docker Setup (Recommended)

The easiest way to run AutoQ is using Docker Compose:

```bash
# Clone the repository
cd AutoQ

# Create environment file
cp backend/.env.example backend/.env

# Edit backend/.env and set your configuration
# At minimum, change SECRET_KEY and JWT_SECRET_KEY

# Start all services
docker-compose up --build
```

Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Option 2: Manual Setup

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Download spaCy model:**
   ```bash
   python -m spacy download en_core_web_sm
   ```

6. **Configure environment:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and configure:
   - `SECRET_KEY` - Change to a secure random string
   - `JWT_SECRET_KEY` - Change to a secure random string
   - `DATABASE_URL` - Set your database connection (default: SQLite)

7. **Run the backend:**
   ```bash
   uvicorn app.main:app --reload
   ```

   Backend will be available at http://localhost:8000

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create environment file (optional):**
   ```bash
   # Create .env file
   echo "VITE_API_URL=http://localhost:8000" > .env
   ```

4. **Run the frontend:**
   ```bash
   npm run dev
   ```

   Frontend will be available at http://localhost:3000

## First Time Setup

1. **Register an account:**
   - Go to http://localhost:3000/register
   - Create an instructor account

2. **Upload a PDF:**
   - Login and navigate to Documents
   - Upload a PDF file (lecture notes, textbook, etc.)

3. **Process the document:**
   - Click "Process" button on the uploaded document
   - Wait for processing to complete

4. **Generate questions:**
   - Navigate to Questions
   - Click "Generate Questions"
   - Select the processed document
   - Configure question types and difficulty
   - Click "Generate"

5. **Create question paper:**
   - Navigate to Question Papers
   - Click "Create Paper"
   - Select questions
   - Configure paper settings
   - Click "Create Paper"

6. **Export:**
   - Click the download icon on any paper
   - Choose PDF or Word format
   - Optionally include answers

## Database Setup (PostgreSQL)

If using PostgreSQL instead of SQLite:

1. **Create database:**
   ```sql
   CREATE DATABASE autoq_db;
   CREATE USER autoq_user WITH PASSWORD 'autoq_password';
   GRANT ALL PRIVILEGES ON DATABASE autoq_db TO autoq_user;
   ```

2. **Update .env:**
   ```
   DATABASE_URL=postgresql://autoq_user:autoq_password@localhost:5432/autoq_db
   ```

## Troubleshooting

### Backend Issues

**Import errors:**
```bash
# Make sure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

**spaCy model not found:**
```bash
python -m spacy download en_core_web_sm
```

**Database errors:**
```bash
# Delete existing database and restart
rm autoq.db  # For SQLite
# Backend will recreate tables on startup
```

### Frontend Issues

**Module not found:**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**API connection errors:**
- Ensure backend is running on port 8000
- Check VITE_API_URL in .env

### Docker Issues

**Port already in use:**
```bash
# Change ports in docker-compose.yml
# Or stop conflicting services
```

**Permission errors:**
```bash
# On Linux, you may need to run with sudo
sudo docker-compose up
```

## Production Deployment

For production deployment:

1. **Change all secret keys** in .env
2. **Set DEBUG=False**
3. **Use PostgreSQL** instead of SQLite
4. **Enable HTTPS**
5. **Set proper ALLOWED_ORIGINS**
6. **Use production-grade web server** (e.g., Gunicorn + Nginx)
7. **Set up proper backup** for database and uploads
8. **Configure file storage** (e.g., S3, Azure Blob)

## Support

For issues and questions:
- Check the documentation in README.md
- Review API documentation at /docs
- Open an issue on GitHub

## License

MIT License - see LICENSE file for details
