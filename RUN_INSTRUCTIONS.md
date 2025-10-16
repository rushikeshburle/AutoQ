# AutoQ - Running Instructions

## Quick Start (Choose One Method)

### Method 1: Docker (Recommended - Easiest)

```bash
# 1. Navigate to project directory
cd AutoQ

# 2. Copy environment file
cp backend/.env.example backend/.env

# 3. Start all services
docker-compose up -d

# 4. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

**To stop:**
```bash
docker-compose down
```

### Method 2: Manual Setup

#### Terminal 1 - Backend

```bash
# Navigate to backend
cd AutoQ/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Copy environment file
cp .env.example .env

# Run backend
uvicorn app.main:app --reload
```

Backend running at: http://localhost:8000

#### Terminal 2 - Frontend

```bash
# Navigate to frontend
cd AutoQ/frontend

# Install dependencies
npm install

# Run frontend
npm run dev
```

Frontend running at: http://localhost:3000

## First Time Usage

### 1. Register Account
- Go to http://localhost:3000/register
- Create an instructor account

### 2. Upload PDF
- Login → Documents → Upload PDF
- Click "Process" after upload

### 3. Generate Questions
- Questions → Generate Questions
- Select document and configure
- Click Generate

### 4. Create Paper
- Question Papers → Create Paper
- Select questions → Create

### 5. Export
- Click download icon → Choose format

## Environment Configuration

### Backend (.env)

Required variables:
```env
SECRET_KEY=your-secret-key-change-this
JWT_SECRET_KEY=your-jwt-secret-change-this
DATABASE_URL=sqlite:///./autoq.db
```

Optional:
```env
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000
```

## Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.9+

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check if port 8000 is free
# Windows: netstat -ano | findstr :8000
# Linux/Mac: lsof -i :8000
```

### Frontend won't start
```bash
# Check Node version
node --version  # Should be 16+

# Clear and reinstall
rm -rf node_modules package-lock.json
npm install

# Check if port 3000 is free
```

### spaCy model error
```bash
python -m spacy download en_core_web_sm
```

### Database errors
```bash
# Delete and recreate (SQLite)
rm autoq.db
# Backend will recreate on next start
```

## Production Deployment

### Important Changes for Production

1. **Change secrets in .env:**
   ```env
   SECRET_KEY=<generate-strong-random-key>
   JWT_SECRET_KEY=<generate-strong-random-key>
   DEBUG=False
   ```

2. **Use PostgreSQL:**
   ```env
   DATABASE_URL=postgresql://user:pass@localhost:5432/autoq_db
   ```

3. **Update CORS:**
   ```env
   ALLOWED_ORIGINS=https://yourdomain.com
   ```

4. **Use production server:**
   ```bash
   # Install gunicorn
   pip install gunicorn
   
   # Run with gunicorn
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

5. **Build frontend:**
   ```bash
   cd frontend
   npm run build
   # Serve dist/ folder with nginx or similar
   ```

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Manual API Testing
Visit http://localhost:8000/docs for interactive API testing

## Useful Commands

### Docker
```bash
# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Rebuild
docker-compose up --build

# Stop and remove
docker-compose down -v
```

### Database
```bash
# Access PostgreSQL (Docker)
docker-compose exec db psql -U autoq_user -d autoq_db

# Backup database
docker-compose exec db pg_dump -U autoq_user autoq_db > backup.sql
```

### Development
```bash
# Backend with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend with specific port
npm run dev -- --port 3001

# Run tests with coverage
pytest --cov=app tests/
```

## System Requirements

### Minimum
- 2 CPU cores
- 4GB RAM
- 10GB storage
- Python 3.9+
- Node.js 16+

### Recommended
- 4+ CPU cores
- 8GB+ RAM
- 50GB+ storage
- SSD for database
- Python 3.11+
- Node.js 18+

## Port Usage

- **3000** - Frontend (React)
- **8000** - Backend (FastAPI)
- **5432** - PostgreSQL (if using Docker)
- **6379** - Redis (if using Docker)

## File Locations

### Uploads
- Docker: Volume `uploads`
- Manual: `backend/uploads/`

### Exports
- Docker: Volume `exports`
- Manual: `backend/exports/`

### Database
- SQLite: `backend/autoq.db`
- PostgreSQL: Docker volume `postgres_data`

## Support

- Documentation: See README.md
- API Docs: http://localhost:8000/docs
- Issues: GitHub Issues

## Next Steps

1. Read [QUICKSTART.md](QUICKSTART.md) for detailed first-time setup
2. Review [FEATURES.md](FEATURES.md) for all features
3. Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API reference
4. See [SETUP.md](SETUP.md) for advanced configuration
