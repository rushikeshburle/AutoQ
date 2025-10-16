from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.models.database import get_db
from app.models.user import User
from app.models.document import Document
from app.models.question import Question, QuestionType, DifficultyLevel, Topic
from app.core.security import get_current_active_user
from app.services.question_generator import QuestionGenerator
from app.services.pdf_processor import PDFProcessor

router = APIRouter()
question_generator = QuestionGenerator()
pdf_processor = PDFProcessor()


class GenerateQuestionsRequest(BaseModel):
    document_id: int
    num_questions: int = 10
    question_types: List[QuestionType] = [QuestionType.MCQ, QuestionType.SHORT_ANSWER]
    difficulty_easy: float = 0.4
    difficulty_medium: float = 0.4
    difficulty_hard: float = 0.2
    topic_ids: Optional[List[int]] = None


class QuestionResponse(BaseModel):
    id: int
    question_text: str
    question_type: QuestionType
    difficulty: DifficultyLevel
    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None
    correct_answer: str
    explanation: Optional[str] = None
    suggested_marks: float
    tags: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class QuestionCreate(BaseModel):
    question_text: str
    question_type: QuestionType
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None
    correct_answer: str
    explanation: Optional[str] = None
    suggested_marks: float = 1.0
    tags: Optional[str] = None
    topic_id: Optional[int] = None
    source_document_id: Optional[int] = None


class QuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    difficulty: Optional[DifficultyLevel] = None
    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    suggested_marks: Optional[float] = None
    tags: Optional[str] = None


@router.post("/generate", response_model=List[QuestionResponse])
async def generate_questions(
    request: GenerateQuestionsRequest,
    db: Session = Depends(get_db)
):
    """Generate questions from a document."""
    
    # Debug logging
    print(f"📝 Generate request received:")
    print(f"   Document ID: {request.document_id}")
    print(f"   Num questions: {request.num_questions}")
    print(f"   Question types: {request.question_types}")
    print(f"   Difficulty mix: Easy={request.difficulty_easy}, Medium={request.difficulty_medium}, Hard={request.difficulty_hard}")
    
    # Get document
    document = db.query(Document).filter(
        Document.id == request.document_id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    if not document.is_processed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Document not yet processed. Please process the document first."
        )
    
    # Get text to generate questions from
    if request.topic_ids:
        # Generate from specific topics
        topics = db.query(Topic).filter(
            Topic.id.in_(request.topic_ids),
            Topic.document_id == request.document_id
        ).all()
        
        if not topics:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Topics not found"
            )
        
        text = " ".join([topic.description for topic in topics])
    else:
        # Generate from entire document
        text = document.extracted_text
    
    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No text available for question generation"
        )
    
    # Generate questions
    difficulty_mix = {
        DifficultyLevel.EASY: request.difficulty_easy,
        DifficultyLevel.MEDIUM: request.difficulty_medium,
        DifficultyLevel.HARD: request.difficulty_hard
    }
    
    try:
        generated_questions = question_generator.generate_questions(
            text=text,
            num_questions=request.num_questions,
            question_types=request.question_types,
            difficulty_mix=difficulty_mix
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate questions: {str(e)}"
        )
    
    # Save questions to database
    saved_questions = []
    for q_data in generated_questions:
        # Calculate hash for duplicate detection
        hash_signature = pdf_processor.calculate_text_hash(q_data['question_text'])
        
        question = Question(
            question_text=q_data['question_text'],
            question_type=q_data['question_type'],
            difficulty=q_data['difficulty'],
            option_a=q_data.get('option_a'),
            option_b=q_data.get('option_b'),
            option_c=q_data.get('option_c'),
            option_d=q_data.get('option_d'),
            correct_answer=q_data['correct_answer'],
            explanation=q_data.get('explanation'),
            suggested_marks=q_data['suggested_marks'],
            source_document_id=document.id,
            creator_id=1,
            hash_signature=hash_signature
        )
        
        db.add(question)
        saved_questions.append(question)
    
    db.commit()
    
    # Refresh all questions
    for question in saved_questions:
        db.refresh(question)
    
    return saved_questions


@router.post("/", response_model=QuestionResponse)
async def create_question(
    question_data: QuestionCreate,
    db: Session = Depends(get_db)
):
    """Create a new question manually."""
    
    # Verify document ownership if provided
    if question_data.source_document_id:
        document = db.query(Document).filter(
            Document.id == question_data.source_document_id
        ).first()
        
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
    
    # Calculate hash
    hash_signature = pdf_processor.calculate_text_hash(question_data.question_text)
    
    question = Question(
        **question_data.dict(),
        creator_id=1,
        hash_signature=hash_signature
    )
    
    db.add(question)
    db.commit()
    db.refresh(question)
    
    return question


@router.get("/", response_model=List[QuestionResponse])
async def list_questions(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    question_type: Optional[QuestionType] = None,
    difficulty: Optional[DifficultyLevel] = None,
    document_id: Optional[int] = None
):
    """List questions with optional filters."""
    
    query = db.query(Question)
    
    if question_type:
        query = query.filter(Question.question_type == question_type)
    
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)
    
    if document_id:
        query = query.filter(Question.source_document_id == document_id)
    
    questions = query.offset(skip).limit(limit).all()
    
    return questions


@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific question."""
    
    question = db.query(Question).filter(
        Question.id == question_id
    ).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    return question


@router.put("/{question_id}", response_model=QuestionResponse)
async def update_question(
    question_id: int,
    question_data: QuestionUpdate,
    db: Session = Depends(get_db)
):
    """Update a question."""
    
    question = db.query(Question).filter(
        Question.id == question_id
    ).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    # Update fields
    update_data = question_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(question, field, value)
    
    # Recalculate hash if question text changed
    if question_data.question_text:
        question.hash_signature = pdf_processor.calculate_text_hash(question_data.question_text)
    
    db.commit()
    db.refresh(question)
    
    return question


@router.delete("/{question_id}")
async def delete_question(
    question_id: int,
    db: Session = Depends(get_db)
):
    """Delete a question."""
    
    question = db.query(Question).filter(
        Question.id == question_id
    ).first()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    db.delete(question)
    db.commit()
    
    return {"message": "Question deleted successfully"}
