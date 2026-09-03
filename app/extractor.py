import re


KNOWN_SKILLS = [
    "Python",
    "Java",
    "SQL",
    "Git",
    "GitHub",
    "REST APIs",
    "Data Structures",
    "Algorithms",
    "Object-Oriented Programming",
    "OOP",
    "FastAPI",
    "Flask",
    "React.js",
    "React",
    "Docker",
    "AWS",
    "Machine Learning",
    "Pandas",
    "NumPy",
    "PostgreSQL",
    "MySQL",
    "MongoDB",
    "Scikit-learn",
    "Unit Testing",
    "HTML",
    "CSS",
    "JavaScript",
    "Database",
    "Problem-Solving",
]


def extract_name(text: str) -> str:
    """Extract candidate name from the resume."""

    match = re.search(
        r"NAME:\s*(.+)",
        text,
        re.IGNORECASE,
    )

    if match:
        return match.group(1).strip()

    return "Unknown"


def extract_skills(text: str) -> list[str]:
    """Extract skills listed under the SKILLS section."""

    match = re.search(
        r"SKILLS:\s*(.*?)(?=\n[A-Z][A-Z ]+:|\Z)",
        text,
        re.IGNORECASE | re.DOTALL,
    )

    if not match:
        return []

    skills_text = match.group(1).replace("\n", " ")

    skills = [
        skill.strip()
        for skill in skills_text.split(",")
        if skill.strip()
    ]

    return skills


def extract_education(text: str) -> str:
    """Extract education information."""

    match = re.search(
        r"EDUCATION:\s*(.*?)(?=\n[A-Z][A-Z ]+:|\Z)",
        text,
        re.IGNORECASE | re.DOTALL,
    )

    if match:
        return match.group(1).strip()

    return "Not specified"


def extract_experience(text: str) -> str:
    """Extract experience information."""

    match = re.search(
        r"EXPERIENCE:\s*(.*?)(?=\n[A-Z][A-Z ]+:|\Z)",
        text,
        re.IGNORECASE | re.DOTALL,
    )

    if match:
        return match.group(1).strip()

    return "Not specified"


def extract_resume_information(text: str) -> dict:
    """Convert raw resume text into structured information."""

    return {
        "name": extract_name(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "experience": extract_experience(text),
    }


def extract_required_skills(job_description: str) -> list[str]:
    """
    Extract skills from the REQUIRED SKILLS section
    of the job description.
    """

    match = re.search(
        r"REQUIRED SKILLS:\s*(.*?)(?=\nPREFERRED SKILLS:|\Z)",
        job_description,
        re.IGNORECASE | re.DOTALL,
    )

    if not match:
        return []

    skills_text = match.group(1)

    found_skills = []

    for skill in KNOWN_SKILLS:
        pattern = rf"(?<!\w){re.escape(skill)}(?!\w)"

        if re.search(
            pattern,
            skills_text,
            re.IGNORECASE,
        ):
            found_skills.append(skill)

    return found_skills