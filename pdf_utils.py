from PyPDF2 import PdfReader
import io
from typing import Tuple

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text content from PDF bytes.
    
    Args:
        pdf_bytes: PDF file content as bytes
        
    Returns:
        Extracted text as a single string
        
    Raises:
        ValueError: If PDF cannot be read or is empty
    """
    try:
        pdf_reader = PdfReader(io.BytesIO(pdf_bytes))
        text_parts = []
        
        for page in pdf_reader.pages:
            content = page.extract_text()
            if content:
                text_parts.append(content)
        
        if not text_parts:
            raise ValueError("PDF contains no extractable text")
        
        return "\n\n".join(text_parts)
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")

def build_context_for_llm(text: str, max_length: int = 100000) -> Tuple[str, bool]:
    """
    Prepare context for LLM, optionally truncating if too long.
    
    Args:
        text: Full extracted text
        max_length: Maximum character length for context
        
    Returns:
        Tuple of (context_string, was_truncated)
    """
    if len(text) <= max_length:
        return text, False
    
    truncated = text[:max_length]
    return truncated, True


