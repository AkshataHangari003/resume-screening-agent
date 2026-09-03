import re
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


SKILL_ALIASES = {
    "oop": "object-oriented programming",
    "object-oriented programming": "object-oriented programming",

    "react": "react",
    "react.js": "react",

    "rest api": "rest apis",
    "rest apis": "rest apis",

    "github": "github, git",
}


def normalize_skill(skill: str) -> str:
    """Normalize skill names and handle common aliases."""

    normalized = skill.lower().strip()

    return SKILL_ALIASES.get(
        normalized,
        normalized,
    )


def calculate_semantic_similarity(
    job_description: str,
    resume_text: str,
) -> float:
    """
    Calculate semantic similarity between a job description
    and a resume.

    Returns a score between 0 and 100.
    """

    embeddings = model.encode(
        [job_description, resume_text],
        normalize_embeddings=True,
    )

    similarity = float(
        np.dot(
            embeddings[0],
            embeddings[1],
        )
    )

    similarity = max(
        0.0,
        min(1.0, similarity),
    )

    return round(
        similarity * 100,
        2,
    )


def load_job_description(file_path: str) -> str:
    """Load the job description from a text file."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Job description not found: {file_path}"
        )

    return path.read_text(
        encoding="utf-8"
    ).strip()


def calculate_skill_match(
    required_skills: list[str],
    candidate_skills: list[str],
) -> float:
    """
    Calculate the percentage of required skills
    found in the candidate's skills.
    """

    required = {
        normalize_skill(skill)
        for skill in required_skills
    }

    candidate = {
        normalize_skill(skill)
        for skill in candidate_skills
    }

    if not required:
        return 0.0

    matched = required.intersection(candidate)

    return round(
        (len(matched) / len(required)) * 100,
        2,
    )


def extract_experience_years(
    experience_text: str,
) -> float:
    """
    Extract approximate years of experience from text.

    Fresh graduates are treated as 0 years.
    """

    text = experience_text.lower()

    if "fresh graduate" in text:
        return 0.0

    month_match = re.search(
        r"(\d+(?:\.\d+)?)\s*months?",
        text,
    )

    year_match = re.search(
        r"(\d+(?:\.\d+)?)\s*years?",
        text,
    )

    total_years = 0.0

    if month_match:
        total_years += (
            float(month_match.group(1)) / 12
        )

    if year_match:
        total_years += float(
            year_match.group(1)
        )

    return round(
        total_years,
        2,
    )


def calculate_experience_score(
    experience_text: str,
) -> float:
    """
    Score experience for a junior role requiring
    0-2 years.
    """

    years = extract_experience_years(
        experience_text
    )

    if years == 0:
        return 70.0

    if years < 1:
        return 85.0

    if years <= 2:
        return 100.0

    if years <= 3:
        return 75.0

    if years <= 5:
        return 50.0

    return 25.0