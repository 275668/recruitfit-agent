from __future__ import annotations


def build_interview_scorecard(interview_questions: list[dict]) -> list[dict]:
    """Create a simple interview scorecard from generated questions."""
    return [
        {
            "skill_name": question["skill_name"],
            "main_question": question["main_question"],
            "evaluation_focus": question["evaluation_focus"],
            "rating_scale": "1 = weak evidence, 3 = acceptable evidence, 5 = strong evidence",
            "interviewer_notes": "",
        }
        for question in interview_questions
    ]


def build_candidate_report(
    jd_text: str,
    resume_text: str,
    requirements: list[dict],
    evidence_items: list[dict],
    match_results: list[dict],
    risk_items: list[dict],
    interview_questions: list[dict],
) -> str:
    """Build the final evidence-grounded candidate report in Markdown."""
    recommendation = _make_recommendation(match_results, risk_items)

    sections = [
        "# RecruitFit Candidate Report",
        "",
        "## Executive Summary",
        "",
        f"- JD length: {len(jd_text.split())} words",
        f"- Resume length: {len(resume_text.split())} words",
        f"- Requirements detected: {len(requirements)}",
        f"- Risks requiring interview verification: {len(risk_items)}",
        "- Decision boundary: This report supports interview preparation only.",
        "",
        "## JD Skill Decomposition",
        "",
        _markdown_table(
            requirements,
            ["skill_name", "skill_category", "importance", "required_keywords"],
        ),
        "",
        "## Resume Evidence Matrix",
        "",
        _markdown_table(
            evidence_items,
            ["skill_name", "skill_category", "resume_evidence", "matched_keywords", "evidence_strength"],
        ),
        "",
        "## Match Scoring",
        "",
        _markdown_table(
            match_results,
            ["skill_name", "skill_category", "match_level", "score", "resume_evidence", "explanation"],
        ),
        "",
        "## Risk Diagnosis",
        "",
        _markdown_table(
            risk_items,
            ["skill_name", "risk_level", "risk_reason", "suggested_verification"],
        ),
        "",
        "## Interview Questions",
        "",
        _markdown_table(
            interview_questions,
            ["skill_name", "main_question", "follow_up_question", "evaluation_focus"],
        ),
        "",
        "## Interview Scorecard",
        "",
        _markdown_table(
            build_interview_scorecard(interview_questions),
            ["skill_name", "main_question", "evaluation_focus", "rating_scale", "interviewer_notes"],
        ),
        "",
        "## Final Recommendation",
        "",
        recommendation,
        "",
        "This recommendation is not a hire or reject decision. It indicates how much additional interview verification is needed.",
    ]

    return "\n".join(sections)


def _make_recommendation(match_results: list[dict], risk_items: list[dict]) -> str:
    if not match_results:
        return "Recommend additional screening"

    high_risks = [item for item in risk_items if item["risk_level"] == "High"]
    total_score = sum(item["score"] for item in match_results)
    max_score = len(match_results) * 3
    score_ratio = total_score / max_score if max_score else 0

    if len(high_risks) >= max(2, len(match_results) // 2):
        return "Recommend cautious review"
    if score_ratio >= 0.7:
        return "Recommend interview"
    return "Recommend additional screening"


def _markdown_table(rows: list[dict], columns: list[str]) -> str:
    if not rows:
        return "_No items found._"

    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []

    for row in rows:
        values = [_format_cell(row.get(column, "")) for column in columns]
        body.append("| " + " | ".join(values) + " |")

    return "\n".join([header, divider, *body])


def _format_cell(value) -> str:
    if isinstance(value, list):
        value = ", ".join(value)
    return str(value).replace("|", "\\|").replace("\n", " ")
