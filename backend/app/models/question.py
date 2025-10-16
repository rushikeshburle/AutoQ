from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum, Float, Table
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.models.database import Base


class QuestionType(str, enum.Enum):
    MCQ = "mcq"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    LONG_ANSWER = "long_answer"
    FILL_BLANK = "fill_blank"
    PROGRAMMING = "programming"


class DifficultyLevel(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


# Association table for many-to-many relationship between questions and question papers
question_paper_questions = Table(
    'question_paper_questions',
    Base.metadata,
    Column('question_paper_id', Integer, ForeignKey('question_papers.id')),
    Column('question_id', Integer, ForeignKey('questions.id')),
    Column('order', Integer),
    Column('marks', Float)
)


class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(Enum(QuestionType), nullable=False)
    difficulty = Column(Enum(DifficultyLevel), default=DifficultyLevel.MEDIUM)
    
    # For MCQ and True/False
    option_a = Column(String)
    option_b = Column(String)
    option_c = Column(String)
    option_d = Column(String)
    correct_answer = Column(Text, nullable=False)
    
    # Model answer/explanation
    explanation = Column(Text)
    suggested_marks = Column(Float, default=1.0)
    
    # Metadata
    topic_id = Column(Integer, ForeignKey("topics.id"))
    source_document_id = Column(Integer, ForeignKey("documents.id"))
    creator_id = Column(Integer, ForeignKey("users.id"))
    
    # Tags for categorization
    tags = Column(String)  # Comma-separated tags
    
    # Duplication tracking
    hash_signature = Column(String, index=True)  # For detecting duplicates
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    topic = relationship("Topic", back_populates="questions")
    source_document = relationship("Document", back_populates="questions")
    creator = relationship("User", back_populates="questions")
    question_papers = relationship("QuestionPaper", secondary=question_paper_questions, back_populates="questions")


class Topic(Base):
    __tablename__ = "topics"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    document_id = Column(Integer, ForeignKey("documents.id"))
    
    # Relationships
    document = relationship("Document", back_populates="topics")
    questions = relationship("Question", back_populates="topic", cascade="all, delete-orphan")
