from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.models.database import get_db
from app.models.user import User
from app.models.question import Question
from app.models.question_paper import QuestionPaper
from app.core.security import get_current_active_user
from app.services.export_service import ExportService
import os

router = APIRouter()
export_service = ExportService()


class CreatePaperRequest(BaseModel):
    title: str
    description: Optional[str] = None
    question_ids: List[int]
    total_marks: float = 100.0
    duration_minutes: int = 60
    instructions: Optional[str] = None
    template_name: str = "standard"
    institution_name: Optional[str] = None
    header_text: Optional[str] = None
    footer_text: Optional[str] = None
    is_practice_mode: bool = False


class QuestionPaperResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    total_marks: float
    duration_minutes: int
    is_published: bool
    is_practice_mode: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class QuestionPaperDetail(QuestionPaperResponse):
    instructions: Optional[str] = None
    template_name: str
    institution_name: Optional[str] = None
    questions: List[dict] = []


class ExportRequest(BaseModel):
    format: str = "pdf"  # pdf or docx
    include_answers: bool = False


@router.post("/", response_model=QuestionPaperResponse)
async def create_question_paper(
    request: CreatePaperRequest,
    db: Session = Depends(get_db)
):
    """Create a new question paper."""
    
    # Verify all questions exist and belong to user
    questions = db.query(Question).filter(
        Question.id.in_(request.question_ids),
        Question.creator_id == 1
    ).all()
    
    if len(questions) != len(request.question_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Some questions not found or don't belong to you"
        )
    
    # Create question paper
    paper = QuestionPaper(
        title=request.title,
        description=request.description,
        total_marks=request.total_marks,
        duration_minutes=request.duration_minutes,
        instructions=request.instructions,
        template_name=request.template_name,
        institution_name=request.institution_name or "Institution Name",
        header_text=request.header_text,
        footer_text=request.footer_text,
        is_practice_mode=request.is_practice_mode,
        creator_id=1
    )
    
    # Add questions to paper
    paper.questions = questions
    
    db.add(paper)
    db.commit()
    db.refresh(paper)
    
    return paper


@router.get("/", response_model=List[QuestionPaperResponse])
async def list_question_papers(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """List all question papers for current user."""
    
    papers = db.query(QuestionPaper).filter(
        QuestionPaper.creator_id == 1
    ).offset(skip).limit(limit).all()
    
    return papers


@router.get("/{paper_id}", response_model=QuestionPaperDetail)
async def get_question_paper(
    paper_id: int,
    db: Session = Depends(get_db)
):
    """Get question paper details."""
    
    paper = db.query(QuestionPaper).filter(
        QuestionPaper.id == paper_id,
        QuestionPaper.creator_id == 1
    ).first()
    
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question paper not found"
        )
    
    # Format questions
    questions_data = []
    for question in paper.questions:
        questions_data.append({
            "id": question.id,
            "question_text": question.question_text,
            "question_type": question.question_type,
            "difficulty": question.difficulty,
            "option_a": question.option_a,
            "option_b": question.option_b,
            "option_c": question.option_c,
            "option_d": question.option_d,
            "correct_answer": question.correct_answer,
            "explanation": question.explanation,
            "suggested_marks": question.suggested_marks
        })
    
    return {
        **paper.__dict__,
        "questions": questions_data
    }


@router.post("/{paper_id}/export")
async def export_question_paper(
    paper_id: int,
    request: ExportRequest,
    db: Session = Depends(get_db)
):
    """Export question paper to PDF or Word."""
    
    # Get paper
    paper = db.query(QuestionPaper).filter(
        QuestionPaper.id == paper_id,
        QuestionPaper.creator_id == 1
    ).first()
    
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question paper not found"
        )
    
    # Prepare questions data
    questions_data = []
    for question in paper.questions:
        questions_data.append({
            "question_text": question.question_text,
            "question_type": question.question_type.value,
            "difficulty": question.difficulty.value,
            "option_a": question.option_a,
            "option_b": question.option_b,
            "option_c": question.option_c,
            "option_d": question.option_d,
            "correct_answer": question.correct_answer,
            "explanation": question.explanation,
            "suggested_marks": question.suggested_marks
        })
    
    # Prepare paper config
    paper_config = {
        "title": paper.title,
        "description": paper.description,
        "total_marks": paper.total_marks,
        "duration_minutes": paper.duration_minutes,
        "instructions": paper.instructions or "Read all questions carefully before answering.",
        "institution_name": paper.institution_name,
        "template_name": paper.template_name
    }
    
    try:
        # Export based on format
        if request.format.lower() == "pdf":
            filepath = export_service.export_to_pdf(
                questions=questions_data,
                paper_config=paper_config,
                include_answers=request.include_answers
            )
            paper.pdf_path = filepath
        elif request.format.lower() == "docx":
            filepath = export_service.export_to_word(
                questions=questions_data,
                paper_config=paper_config,
                include_answers=request.include_answers
            )
            paper.docx_path = filepath
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid format. Use 'pdf' or 'docx'"
            )
        
        db.commit()
        
        # Return file
        filename = os.path.basename(filepath)
        return FileResponse(
            filepath,
            media_type="application/octet-stream",
            filename=filename
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export question paper: {str(e)}"
        )


@router.post("/{paper_id}/publish")
async def publish_question_paper(
    paper_id: int,
    db: Session = Depends(get_db)
):
    """Publish a question paper."""
    
    paper = db.query(QuestionPaper).filter(
        QuestionPaper.id == paper_id,
        QuestionPaper.creator_id == 1
    ).first()
    
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question paper not found"
        )
    
    paper.is_published = True
    db.commit()
    
    return {"message": "Question paper published successfully"}


@router.delete("/{paper_id}")
async def delete_question_paper(
    paper_id: int,
    db: Session = Depends(get_db)
):
    """Delete a question paper."""
    
    paper = db.query(QuestionPaper).filter(
        QuestionPaper.id == paper_id,
        QuestionPaper.creator_id == 1
    ).first()
    
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question paper not found"
        )
    
    # Delete exported files
    if paper.pdf_path and os.path.exists(paper.pdf_path):
        try:
            os.remove(paper.pdf_path)
        except:
            pass
    
    if paper.docx_path and os.path.exists(paper.docx_path):
        try:
            os.remove(paper.docx_path)
        except:
            pass
    
    db.delete(paper)
    db.commit()
    
    return {"message": "Question paper deleted successfully"}


@router.put("/{paper_id}", response_model=QuestionPaperResponse)
async def update_question_paper(
    paper_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    total_marks: Optional[float] = None,
    duration_minutes: Optional[int] = None,
    instructions: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Update question paper details."""
    
    paper = db.query(QuestionPaper).filter(
        QuestionPaper.id == paper_id,
        QuestionPaper.creator_id == 1
    ).first()
    
    if not paper:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question paper not found"
        )
    
    if title:
        paper.title = title
    if description:
        paper.description = description
    if total_marks:
        paper.total_marks = total_marks
    if duration_minutes:
        paper.duration_minutes = duration_minutes
    if instructions:
        paper.instructions = instructions
    
    db.commit()
    db.refresh(paper)
    
    return paper
