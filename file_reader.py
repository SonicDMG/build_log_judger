import docx
import fitz  # PyMuPDF
import re

def read_docx(file):
    doc = docx.Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return '\n'.join(full_text)

def read_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    full_text = []
    for page in doc:
        text = page.get_text("text")
        full_text.append(text)
    return '\n'.join(full_text)

def read_txt(file):
    content = file.read().decode("utf-8")
    # Remove image links (assuming they are URLs)
    content = re.sub(r'http[s]?://\S+\.(?:jpg|jpeg|png|gif)', '', content)
    return content

def read_md(file):
    content = file.read().decode("utf-8")
    # Remove Markdown image syntax ![alt text](image_url) and base64-encoded images
    content = re.sub(r'!\[.*?\]\(.*?\)', '', content)
    content = re.sub(r'\[.*?\]:\s*<data:image\/.*?;base64,.*?>', '', content)
    return content

def read_file(file, file_type):
    if file_type == "docx":
        return read_docx(file)
    elif file_type == "pdf":
        return read_pdf(file)
    elif file_type == "txt":
        return read_txt(file)
    elif file_type == "md":
        return read_md(file)
    else:
        return "Unsupported file type"