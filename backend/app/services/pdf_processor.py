import fitz  # PyMuPDF
from typing import List, Dict, Tuple
import re
from pathlib import Path
import hashlib


class PDFProcessor:
    """Service for extracting text and metadata from PDF files."""
    
    def __init__(self):
        self.min_text_length = 50
    
    def extract_text(self, pdf_path: str) -> str:
        """Extract all text from a PDF file."""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text += page.get_text()
            
            doc.close()
            return self._clean_text(text)
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def extract_text_by_pages(self, pdf_path: str) -> List[Dict[str, any]]:
        """Extract text from PDF with page information."""
        try:
            doc = fitz.open(pdf_path)
            pages = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                
                pages.append({
                    "page_number": page_num + 1,
                    "text": self._clean_text(text),
                    "word_count": len(text.split())
                })
            
            doc.close()
            return pages
        except Exception as e:
            raise Exception(f"Error extracting text by pages: {str(e)}")
    
    def extract_metadata(self, pdf_path: str) -> Dict[str, any]:
        """Extract metadata from PDF."""
        try:
            doc = fitz.open(pdf_path)
            metadata = doc.metadata
            
            info = {
                "title": metadata.get("title", ""),
                "author": metadata.get("author", ""),
                "subject": metadata.get("subject", ""),
                "keywords": metadata.get("keywords", ""),
                "creator": metadata.get("creator", ""),
                "producer": metadata.get("producer", ""),
                "page_count": len(doc),
                "file_size": Path(pdf_path).stat().st_size
            }
            
            doc.close()
            return info
        except Exception as e:
            raise Exception(f"Error extracting metadata: {str(e)}")
    
    def detect_sections(self, text: str) -> List[Dict[str, str]]:
        """Detect sections/chapters in the text based on headings."""
        sections = []
        
        # Common heading patterns
        heading_patterns = [
            r'^(Chapter|CHAPTER)\s+\d+[:\.\s]+(.+)$',
            r'^(\d+\.\s+)([A-Z][^.!?]*?)$',
            r'^([A-Z][A-Z\s]{3,}?)$',  # ALL CAPS headings
            r'^(Unit|UNIT)\s+\d+[:\.\s]+(.+)$',
        ]
        
        lines = text.split('\n')
        current_section = {"title": "Introduction", "content": ""}
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            is_heading = False
            for pattern in heading_patterns:
                match = re.match(pattern, line, re.MULTILINE)
                if match:
                    # Save previous section
                    if current_section["content"].strip():
                        sections.append(current_section)
                    
                    # Start new section
                    current_section = {
                        "title": line,
                        "content": ""
                    }
                    is_heading = True
                    break
            
            if not is_heading:
                current_section["content"] += line + " "
        
        # Add last section
        if current_section["content"].strip():
            sections.append(current_section)
        
        # If no sections detected, treat entire text as one section
        if not sections:
            sections.append({
                "title": "Main Content",
                "content": text
            })
        
        return sections
    
    def extract_key_concepts(self, text: str, top_n: int = 20) -> List[str]:
        """Extract key concepts/terms from text using simple frequency analysis."""
        # Remove common words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these',
            'those', 'it', 'its', 'they', 'their', 'them', 'we', 'our', 'us'
        }
        
        # Extract words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Count frequencies
        word_freq = {}
        for word in words:
            if word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        return [word for word, freq in sorted_words[:top_n]]
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page numbers (simple pattern)
        text = re.sub(r'\n\d+\n', '\n', text)
        
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s.,;:!?()\-\'"]+', '', text)
        
        return text.strip()
    
    def calculate_text_hash(self, text: str) -> str:
        """Calculate hash of text for duplicate detection."""
        return hashlib.md5(text.encode()).hexdigest()
    
    def split_into_chunks(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split text into overlapping chunks for processing."""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if len(chunk) > self.min_text_length:
                chunks.append(chunk)
        
        return chunks
