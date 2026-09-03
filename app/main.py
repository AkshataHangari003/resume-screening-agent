from pathlib import Path
import csv
import json

from parser import load_resumes

from extractor import (
    extract_resume_information,
    extract_required_skills,
)

from scorer import (
    calculate_semantic_similarity,
    calculate_skill_match,
    calculate_experience_score,
    load_job_description,
)

from ranker import (
    get_matched_skills,
    get_missing_skills,
    generate_recommendation,
    generate_reason,
)


BASE_DIR = Path(__file__).resolve().parent.parent

RESUME_DIR = BASE_DIR / "data" / "resumes"
JD_FILE = BASE_DIR / "data" / "job_description.txt"
OUTPUT_DIR = BASE_DIR / "output"


# Final score weights
SEMANTIC_WEIGHT = 0.50
SKILL_WEIGHT = 0.30
EXPERIENCE_WEIGHT = 0.20


def calculate_final_score(
    semantic_score: float,
    skill_score: float,
    experience_score: float,
) -> float:
    """Calculate the final candidate score out of 100."""

    final_score = (
        semantic_score * SEMANTIC_WEIGHT
        + skill_score * SKILL_WEIGHT
        + experience_score * EXPERIENCE_WEIGHT
    )

    return round(final_score, 2)


def save_json(results: list[dict]) -> None:
    """Save ranked results as JSON."""

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        OUTPUT_DIR / "ranked_candidates.json"
    )

    with output_file.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False,
        )


def save_csv(results: list[dict]) -> None:
    """Save ranked results as CSV."""

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        OUTPUT_DIR / "ranked_candidates.csv"
    )

    fieldnames = [
        "rank",
        "name",
        "filename",
        "final_score",
        "semantic_score",
        "skill_score",
        "experience_score",
        "matched_skills",
        "missing_skills",
        "education",
        "experience",
        "recommendation",
        "reason",
    ]

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for rank, candidate in enumerate(
            results,
            start=1,
        ):

            writer.writerow(
                {
                    "rank": rank,
                    "name": candidate["name"],
                    "filename": candidate["filename"],
                    "final_score": candidate["final_score"],
                    "semantic_score": candidate[
                        "semantic_score"
                    ],
                    "skill_score": candidate[
                        "skill_score"
                    ],
                    "experience_score": candidate[
                        "experience_score"
                    ],
                    "matched_skills": ", ".join(
                        candidate["matched_skills"]
                    ),
                    "missing_skills": ", ".join(
                        candidate["missing_skills"]
                    ),
                    "education": candidate[
                        "education"
                    ],
                    "experience": candidate[
                        "experience"
                    ],
                    "recommendation": candidate[
                        "recommendation"
                    ],
                    "reason": candidate["reason"],
                }
            )


def main():

    # -----------------------------------
    # 1. Load Job Description
    # -----------------------------------

    job_description = load_job_description(
        str(JD_FILE)
    )


    # -----------------------------------
    # 2. Extract Required Skills
    # -----------------------------------

    required_skills = extract_required_skills(
        job_description
    )


    # -----------------------------------
    # 3. Load Resumes
    # -----------------------------------

    resumes = load_resumes(
        str(RESUME_DIR)
    )


    print(
        f"Found {len(resumes)} resumes."
    )

    print(
        f"Required skills: {required_skills}"
    )

    print(
        "\nCalculating final candidate scores...\n"
    )


    results = []


    # -----------------------------------
    # 4. Process Resumes
    # -----------------------------------

    for resume in resumes:

        information = extract_resume_information(
            resume["text"]
        )


        semantic_score = (
            calculate_semantic_similarity(
                job_description,
                resume["text"],
            )
        )


        skill_score = calculate_skill_match(
            required_skills,
            information["skills"],
        )


        experience_score = (
            calculate_experience_score(
                information["experience"]
            )
        )


        final_score = calculate_final_score(
            semantic_score,
            skill_score,
            experience_score,
        )


        # -----------------------------------
        # Candidate Reasoning
        # -----------------------------------

        matched_skills = get_matched_skills(
            required_skills,
            information["skills"],
        )


        missing_skills = get_missing_skills(
            required_skills,
            information["skills"],
        )


        recommendation = generate_recommendation(
            final_score
        )


        reason = generate_reason(
            matched_skills,
            missing_skills,
            information["experience"],
            recommendation,
        )


        results.append(
            {
                "name": information["name"],
                "filename": resume["filename"],
                "semantic_score": semantic_score,
                "skill_score": skill_score,
                "experience_score": experience_score,
                "final_score": final_score,
                "skills": information["skills"],
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "education": information["education"],
                "experience": information["experience"],
                "recommendation": recommendation,
                "reason": reason,
            }
        )


    # -----------------------------------
    # 5. Rank Candidates
    # -----------------------------------

    results.sort(
        key=lambda candidate: candidate[
            "final_score"
        ],
        reverse=True,
    )


    # -----------------------------------
    # 6. Add Rank
    # -----------------------------------

    for rank, candidate in enumerate(
        results,
        start=1,
    ):
        candidate["rank"] = rank


    # -----------------------------------
    # 7. Save Output Files
    # -----------------------------------

    save_json(results)
    save_csv(results)


    # -----------------------------------
    # 8. Display Results
    # -----------------------------------

    print("=" * 90)
    print("FINAL RESUME SCREENING RESULTS")
    print("=" * 90)


    for candidate in results:

        print(
            f"\nRank: {candidate['rank']}"
        )

        print(
            f"Candidate: "
            f"{candidate['name']}"
        )

        print(
            f"Final Score: "
            f"{candidate['final_score']:.2f}/100"
        )

        print(
            f"Semantic Score: "
            f"{candidate['semantic_score']:.2f}/100"
        )

        print(
            f"Skill Match: "
            f"{candidate['skill_score']:.2f}/100"
        )

        print(
            f"Experience Score: "
            f"{candidate['experience_score']:.2f}/100"
        )

        print(
            f"Education: "
            f"{candidate['education']}"
        )

        print(
            f"Experience: "
            f"{candidate['experience']}"
        )

        print(
            f"Skills: "
            f"{', '.join(candidate['skills'])}"
        )

        print(
            f"Matched Skills: "
            f"{', '.join(candidate['matched_skills']) or 'None'}"
        )

        print(
            f"Missing Skills: "
            f"{', '.join(candidate['missing_skills']) or 'None'}"
        )

        print(
            f"Recommendation: "
            f"{candidate['recommendation']}"
        )

        print(
            f"Reason: "
            f"{candidate['reason']}"
        )


    print("\n" + "=" * 90)
    print("OUTPUT FILES")
    print("=" * 90)

    print(
        f"JSON: {OUTPUT_DIR / 'ranked_candidates.json'}"
    )

    print(
        f"CSV:  {OUTPUT_DIR / 'ranked_candidates.csv'}"
    )


if __name__ == "__main__":
    main()