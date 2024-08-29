import docx
import fitz  # PyMuPDF

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
    return file.read().decode("utf-8")

def read_md(file):
    return file.read().decode("utf-8")

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