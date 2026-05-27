from __future__ import annotations


def analyze_risks(match_results: list[dict]) -> list[dict]:
    """Generate risk items for missing or only medium-strength evidence."""
    risk_items = []

    for result in match_results:
        if result["match_level"] == "No Evidence":
            risk_items.append(
                {
                    "skill_name": result["skill_name"],
                    "risk_level": "High",
                    "risk_reason": "No explicit resume evidence found for this required skill.",
                    "suggested_verification": (
                        f"Ask the candidate to provide a concrete example involving "
                        f"{result['skill_name']}."
                    ),
                }
            )
        elif result["match_level"] == "Medium Match":
            risk_items.append(
                {
                    "skill_name": result["skill_name"],
                    "risk_level": "Medium",
                    "risk_reason": "Some evidence exists, but it may not prove depth, ownership, or outcomes.",
                    "suggested_verification": (
                        f"Verify the candidate's role, scope, and measurable impact in "
                        f"{result['skill_name']} work."
                    ),
                }
            )

    return risk_items
