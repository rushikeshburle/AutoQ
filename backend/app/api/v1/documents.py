from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
import os
import uuid
from datetime import datetime
from app.models.database import get_db
from app.models.user import User
from app.models.document import Document
from app.models.question import Topic
from app.core.security import get_current_active_user
from app.core.config import settings
from app.services.pdf_processor import PDFProcessor
from app.services.nlp_engine import NLPEngine

router = APIRouter()
pdf_processor = PDFProcessor()
nlp_engine = NLPEngine()


class DocumentResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_size: int
    is_processed: bool
    processing_status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class DocumentDetail(DocumentResponse):
    extracted_text: str = None
    topics: List[dict] = []


class TopicResponse(BaseModel):
    id: int
    name: str
    description: str
    
    class Config:
        from_attributes = True


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a PDF document for processing (No auth required)."""
    
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )
    
    # Check file size
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE} bytes"
        )
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    # Save file
    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )
    
    # Create document record
    document = Document(
        filename=unique_filename,
        original_filename=file.filename,
        file_path=file_path,
        file_size=file_size,
        mime_type="application/pdf",
        owner_id=1,  # Default user for no-auth mode
        processing_status="pending"
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    return document


@router.post("/{document_id}/process")
async def process_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """Process a document to extract text and topics (No auth required)."""
    
    # Get document
    document = db.query(Document).filter(
        Document.id == document_id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    if document.is_processed:
        return {"message": "Document already processed", "document_id": document_id}
    
    try:
        # Update status
        document.processing_status = "processing"
        db.commit()
        
        # Extract text
        extracted_text = pdf_processor.extract_text(document.file_path)
        document.extracted_text = extracted_text
        
        # Detect sections/topics
        sections = pdf_processor.detect_sections(extracted_text)
        
        # Create topic records
        for section in sections:
            topic = Topic(
                name=section['title'],
                description=section['content'][:500],  # First 500 chars
                document_id=document.id
            )
            db.add(topic)
        
        # Mark as processed
        document.is_processed = True
        document.processing_status = "completed"
        
        db.commit()
        db.refresh(document)
        
        return {
            "message": "Document processed successfully",
            "document_id": document_id,
            "topics_found": len(sections)
        }
        
    except Exception as e:
        document.processing_status = "failed"
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process document: {str(e)}"
        )


@router.get("/", response_model=List[DocumentResponse])
async def list_documents(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """List all documents (No auth required)."""
    
    documents = db.query(Document).offset(skip).limit(limit).all()
    
    return documents


@router.get("/{document_id}", response_model=DocumentDetail)
async def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """Get document details (No auth required)."""
    
    document = db.query(Document).filter(
        Document.id == document_id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Get topics
    topics = db.query(Topic).filter(Topic.document_id == document_id).all()
    
    return {
        **document.__dict__,
        "topics": [{"id": t.id, "name": t.name, "description": t.description} for t in topics]
    }


@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a document."""
    
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.owner_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Delete file
    try:
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
    except Exception as e:
        print(f"Warning: Failed to delete file: {str(e)}")
    
    # Delete database record
    db.delete(document)
    db.commit()
    
    return {"message": "Document deleted successfully"}


@router.get("/{document_id}/topics", response_model=List[TopicResponse])
async def get_document_topics(
    document_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get topics for a document."""
    
    # Verify document ownership
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.owner_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    topics = db.query(Topic).filter(Topic.document_id == document_id).all()
    
    return topics
