"""
This script provides functions to read the content of various file types.

The supported file types are:
1. DOCX (Microsoft Word)
2. PDF (Portable Document Format)
3. TXT (Plain Text)
4. MD (Markdown)

The script uses the following libraries:
- `docx` for reading DOCX files.
- `fitz` (PyMuPDF) for reading PDF files.
- `re` for regular expression operations.
- `coloredlogs` for enhanced logging.

Functions:
- `read_file(file, file_type)`: Reads the content of a file based on its type.
- `read_docx(file)`: Reads the content of a DOCX file.
- `read_pdf(file)`: Reads the content of a PDF file.
- `read_txt(file)`: Reads the content of a TXT file.
- `read_md(file)`: Reads the content of a Markdown file.

Logging:
- Configured to log at the DEBUG level using `coloredlogs`.

Example usage:
    content = read_file(uploaded_file, 'pdf')
"""
import logging
import re
import coloredlogs
from docx import Document
import fitz  # PyMuPDF

# Configure logger
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)

def read_file(file, file_type):
    """Read the content of a file based on its type."""
    try:
        if file_type == 'docx':
            return read_docx(file)
        elif file_type == 'pdf':
            return read_pdf(file)
        elif file_type == 'txt':
            return read_txt(file)
        elif file_type == 'md':
            return read_md(file)
        else:
            logger.error("Unsupported file type: %s", file_type)
            raise ValueError(f"Unsupported file type: {file_type}")
    except Exception as e:
        logger.error("Error reading file: %s", e)
        raise

def read_docx(file):
    """Read the content of a DOCX file."""
    try:
        doc = Document(file)
        content = '\n'.join([para.text for para in doc.paragraphs])
        logger.debug("Read DOCX file: %s", file)
        return content
    except Exception as e:
        logger.error("Error reading DOCX file: %s", e)
        raise

def read_pdf(file):
    """Read the content of a PDF file."""
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        full_text = []
        for page in doc:
            text = page.get_text("text")
            full_text.append(text)
        logger.debug("Read PDF file: %s", file)
        return '\n'.join(full_text)
    except Exception as e:
        logger.error("Error reading PDF file: %s", e)
        raise

def read_txt(file):
    """Read the content of a TXT file."""
    try:
        content = file.read().decode('utf-8')
        logger.debug("Read TXT file: %s", file)
        return content
    except Exception as e:
        logger.error("Error reading TXT file: %s", e)
        raise

def read_md(file):
    """Read the content of a Markdown file."""
    try:
        content = file.read().decode("utf-8")
        # Remove Markdown image syntax ![alt text](image_url) and base64-encoded images
        content = re.sub(r'!\[.*?\]\(.*?\)', '', content)
        content = re.sub(r'\[.*?\]:\s*<data:image\/.*?;base64,.*?>', '', content)
        logger.debug("Read MD file: %s", file)
        return content
    except Exception as e:
        logger.error("Error reading MD file: %s", e)
        raise
