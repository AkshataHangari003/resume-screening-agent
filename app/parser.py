from pathlib import Path

import pymupdf
from docx import Document


def extract_text_from_pdf(file_path: Path) -> str:
    """Extract text from a PDF file."""
    text = []

    with pymupdf.open(file_path) as pdf:
        for page in pdf:
            text.append(page.get_text())

    return "\n".join(text).strip()


def extract_text_from_docx(file_path: Path) -> str:
    """Extract text from a DOCX file."""
    document = Document(file_path)

    paragraphs = [
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(paragraphs).strip()


def extract_text_from_txt(file_path: Path) -> str:
    """Extract text from a TXT file."""
    return file_path.read_text(encoding="utf-8").strip()


def extract_resume_text(file_path: str) -> str:
    """
    Extract text from a resume based on its file extension.

    Supported formats:
    - TXT
    - PDF
    - DOCX
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Resume not found: {file_path}")

    extension = path.suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(path)

    if extension == ".docx":
        return extract_text_from_docx(path)

    if extension == ".txt":
        return extract_text_from_txt(path)

    raise ValueError(
        f"Unsupported file format: {extension}. "
        "Use PDF, DOCX, or TXT."
    )


def load_resumes(resume_directory: str) -> list[dict]:
    """Load all supported resumes from a directory."""
    directory = Path(resume_directory)

    if not directory.exists():
        raise FileNotFoundError(
            f"Resume directory not found: {resume_directory}"
        )

    supported_extensions = {".pdf", ".docx", ".txt"}

    resumes = []

    for file_path in sorted(directory.iterdir()):
        if (
            file_path.is_file()
            and file_path.suffix.lower() in supported_extensions
        ):
            text = extract_resume_text(str(file_path))

            resumes.append(
                {
                    "filename": file_path.name,
                    "text": text,
                }
            )

    return resumes