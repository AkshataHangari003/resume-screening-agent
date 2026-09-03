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

    matched_count = len(matched_skills)
    missing_count = len(missing_skills)
    total_skills = matched_count + missing_count

    if total_skills > 0:
        skill_match_percentage = (
            matched_count / total_skills
        ) * 100
    else:
        skill_match_percentage = 0.0

    if missing_skills:
        missing_text = ", ".join(missing_skills)
        skill_reason = (
            f"Required skill match: "
            f"{skill_match_percentage:.2f}%. "
            f"Missing required skills: {missing_text}."
        )
    else:
        skill_reason = (
            "Required skill match: 100%. "
            "No required skills are missing."
        )

    return (
        f"{recommendation}. "
        f"{skill_reason} "
        f"Experience: {experience_text}."
    )