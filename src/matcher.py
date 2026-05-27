from __future__ import annotations


def score_matches(evidence_items: list[dict]) -> list[dict]:
    """Convert resume evidence into evidence-grounded match scores."""
    match_results = []

    for item in evidence_items:
        evidence_strength = item["evidence_strength"]
        match_level, score = _score_from_strength(evidence_strength)

        match_results.append(
            {
                "skill_name": item["skill_name"],
                "skill_category": item["skill_category"],
                "resume_evidence": item["resume_evidence"],
                "evidence_strength": evidence_strength,
                "match_level": match_level,
                "score": score,
                "explanation": _build_explanation(item, match_level),
            }
        )

    return match_results


def _score_from_strength(evidence_strength: str) -> tuple[str, int]:
    if evidence_strength == "Strong":
        return "Strong Match", 3
    if evidence_strength == "Medium":
        return "Medium Match", 2
    if evidence_strength == "Weak":
        return "Weak Match", 1
    return "No Evidence", 0


def _build_explanation(item: dict, match_level: str) -> str:
    if item["resume_evidence"] == "No evidence found":
        return "No explicit resume evidence was found for this JD requirement."

    keywords = ", ".join(item["matched_keywords"])
    return (
        f"{match_level} because the resume evidence explicitly contains "
        f"matched keyword(s): {keywords}."
    )
