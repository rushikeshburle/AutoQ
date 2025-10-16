from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.models.database import init_db
from app.api.v1 import auth, documents, questions, papers
import os

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Automatic Question Paper Generator - Transform PDFs into question papers",
)

# CORS middleware - Allow all origins for simple frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs("./exports", exist_ok=True)

# Mount static files
if os.path.exists("./exports"):
    app.mount("/exports", StaticFiles(directory="./exports"), name="exports")

# Custom validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors with detailed messages."""
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(x) for x in error["loc"])
        message = error["msg"]
        error_type = error["type"]
        errors.append(f"{field}: {message} (type: {error_type})")
    
    error_detail = "; ".join(errors)
    print(f"❌ Validation Error: {error_detail}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": f"Validation error: {error_detail}",
            "errors": exc.errors()
        }
    )

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["Documents"])
app.include_router(questions.router, prefix="/api/v1/questions", tags=["Questions"])
app.include_router(papers.router, prefix="/api/v1/papers", tags=["Question Papers"])


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} started successfully!")
    print(f"📚 Database initialized")
    print(f"🌐 CORS enabled for: {settings.ALLOWED_ORIGINS}")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }
