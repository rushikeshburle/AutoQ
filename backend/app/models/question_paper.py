from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.database import Base
from app.models.question import question_paper_questions


class QuestionPaper(Base):
    __tablename__ = "question_papers"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    
    # Configuration
    total_marks = Column(Float, default=100.0)
    duration_minutes = Column(Integer, default=60)
    instructions = Column(Text)
    
    # Template and branding
    template_name = Column(String, default="standard")
    institution_name = Column(String)
    header_text = Column(Text)
    footer_text = Column(Text)
    
    # Status
    is_published = Column(Boolean, default=False)
    is_practice_mode = Column(Boolean, default=False)
    
    # Metadata
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Export tracking
    pdf_path = Column(String)
    docx_path = Column(String)
    
    # Relationships
    creator = relationship("User", back_populates="question_papers")
    questions = relationship("Question", secondary=question_paper_questions, back_populates="question_papers")
