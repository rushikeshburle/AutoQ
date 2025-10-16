# Changelog

All notable changes to AutoQ will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-01

### Added
- Initial release of AutoQ
- PDF document upload and processing
- Automatic text extraction from PDFs
- Topic and section detection
- Intelligent question generation with multiple types:
  - Multiple Choice Questions (MCQ)
  - True/False questions
  - Short Answer questions
  - Long Answer questions
  - Fill in the Blanks
  - Programming questions
- Difficulty level assignment (Easy, Medium, Hard)
- Question bank management
- Question paper creation and configuration
- PDF and Word export functionality
- Answer key generation
- User authentication and authorization
- Role-based access control (Admin, Instructor, Student)
- Modern React frontend with TailwindCSS
- FastAPI backend with SQLAlchemy ORM
- Docker support for easy deployment
- Comprehensive API documentation
- Setup and user guides

### Features
- NLP-powered question generation using spaCy
- Customizable difficulty distribution
- Topic-aware question generation
- Question duplicate detection
- Printable question paper templates
- Institution branding support
- Secure JWT authentication
- RESTful API architecture
- Responsive web interface

### Technical
- Python 3.9+ backend
- React 18 with TypeScript frontend
- PostgreSQL/SQLite database support
- PyMuPDF for PDF processing
- ReportLab for PDF generation
- python-docx for Word export
- Docker and Docker Compose support

## [Unreleased]

### Planned
- Transformer-based question generation (T5, BART)
- Student practice mode with instant feedback
- Performance analytics and reporting
- Question quality scoring
- Multi-language support
- LMS integration (Moodle, Canvas)
- Collaborative question bank sharing
- Advanced export templates
- Question versioning
- Bloom's Taxonomy classification
- Image support in questions
- LaTeX math equation support
- Bulk operations
- Question import from various formats
- Mobile app
