from scorer import normalize_skill


def get_matched_skills(
    required_skills: list[str],
    candidate_skills: list[str],
) -> list[str]:
    """Return required skills matched by the candidate."""

    required = {
        normalize_skill(skill): skill
        for skill in required_skills
    }

    candidate = {
        normalize_skill(skill)
        for skill in candidate_skills
    }

    matched = [
        original
        for normalized, original in required.items()
        if normalized in candidate
    ]

    return matched


def get_missing_skills(
    required_skills: list[str],
    candidate_skills: list[str],
) -> list[str]:
    """Return required skills missing from the candidate."""

    required = {
        normalize_skill(skill): skill
        for skill in required_skills
    }

    candidate = {
        normalize_skill(skill)
        for skill in candidate_skills
    }

    missing = [
        original
        for normalized, original in required.items()
        if normalized not in candidate
    ]

    return missing


def generate_recommendation(
    final_score: float,
) -> str:
    """Generate a recommendation based on final score."""

    if final_score >= 80:
        return "Strong Match"

    if final_score >= 65:
        return "Good Match"

    if final_score >= 50:
        return "Moderate Match"

    return "Weak Match"


def generate_reason(
    matched_skills: list[str],
    missing_skills: list[str],
    experience_text: str,
    recommendation: str,
) -> str:
    """Generate a concise explanation for the ranking."""

    if missing_skills:
        missing_text = ", ".join(
            missing_skills
        )

        skill_reason = (
            f"Missing required skills: "
            f"{missing_text}."
        )
    else:
        skill_reason = (
            "Matches all required skills."
        )

    return (
        f"{recommendation}. "
        f"{skill_reason} "
        f"Experience: {experience_text}."
    )