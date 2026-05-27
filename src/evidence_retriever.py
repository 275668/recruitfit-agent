from __future__ import annotations

import re


GENERIC_TERMS = {
    "analysis",
    "data",
    "product",
    "project",
    "ai",
    "model",
}

SKILL_SPECIFIC_TERMS = {
    "prd",
    "prds",
    "product requirement",
    "product requirements",
    "user story",
    "user stories",
    "prototype",
    "wireframe",
    "figma",
    "agent system",
    "agent workflow",
    "ticket agent",
    "ai agent",
    "agentic",
    "autonomous agent",
    "llm",
    "large language model",
    "prompt engineering",
    "prompt design",
    "rag",
    "retrieval augmented generation",
    "workflow",
    "multi-stage",
    "pipeline",
    "orchestration",
    "python",
    "streamlit",
    "sql",
    "growth analysis",
    "analytics",
    "dashboard",
    "dashboards",
    "product dashboards",
    "a/b testing",
    "ab testing",
    "experiment",
    "controlled test",
    "evaluation metric",
    "metrics",
    "kpi",
    "success metric",
    "cross-functional",
    "stakeholder",
    "stakeholders",
    "communication",
    "communicated",
    "collaborated",
    "hiring",
    "interview",
    "screening",
    "candidate",
    "hr tech",
    "recruiting",
    "recruitment",
    "talent acquisition",
}


def split_resume_into_sentences(resume_text: str) -> list[str]:
    """Split resume text into clean sentence-like units.

    This is a lightweight retrieval baseline for the rule-based MVP. It handles
    periods, semicolons, bullet-like lines, and newline-separated resume entries
    without requiring external NLP libraries.
    """
    normalized_lines = []
    for line in resume_text.splitlines():
        cleaned = re.sub(r"^\s*[-*•\d.)]+\s*", "", line.strip())
        if cleaned:
            normalized_lines.append(cleaned)

    normalized_text = " ".join(normalized_lines)
    normalized_text = re.sub(r"\s+", " ", normalized_text).strip()
    if not normalized_text:
        return []

    return [
        sentence.strip(" -")
        for sentence in re.split(r"(?<=[.!?])\s+|;\s+", normalized_text)
        if sentence.strip(" -")
    ]


def retrieve_candidate_evidence(
    resume_text: str,
    requirements: list[dict],
    top_k: int = 3,
) -> dict:
    """Retrieve top candidate evidence sentences for each requirement.

    This retrieval layer does not force or change final match judgments. It is
    designed to support human evidence review before interviews, not automatic
    hiring decisions. Later versions can replace this deterministic baseline
    with embedding-based retrieval or vector search while preserving the same
    evidence-grounded product boundary.
    """
    sentences = split_resume_into_sentences(resume_text)
    retrieval_results = {}

    for requirement in requirements:
        skill_name = requirement["skill_name"]
        scored_sentences = []

        for sentence in sentences:
            score, matched_terms = _score_sentence(sentence, requirement)
            if score > 0:
                scored_sentences.append(
                    {
                        "sentence": sentence,
                        "score": round(score, 3),
                        "matched_terms": matched_terms,
                    }
                )

        scored_sentences.sort(
            key=lambda item: (item["score"], len(item["matched_terms"])),
            reverse=True,
        )
        retrieval_results[skill_name] = scored_sentences[:top_k]

    return retrieval_results


def _score_sentence(sentence: str, requirement: dict) -> tuple[float, list[str]]:
    sentence_lower = sentence.lower()
    matched_terms = []
    score = 0.0

    for keyword in requirement["required_keywords"]:
        keyword_lower = keyword.lower()
        if not _contains_term(sentence_lower, keyword_lower):
            continue

        matched_terms.append(keyword)
        score += 1.0

        if " " in keyword_lower:
            score += 1.0
        if keyword_lower in SKILL_SPECIFIC_TERMS:
            score += 0.75
        if keyword_lower in GENERIC_TERMS:
            score -= 0.5

    unique_terms = sorted(set(matched_terms))
    if unique_terms and all(term.lower() in GENERIC_TERMS for term in unique_terms):
        score = min(score, 0.5)

    return max(score, 0.0), unique_terms


def _contains_term(sentence_lower: str, term_lower: str) -> bool:
    escaped_term = re.escape(term_lower)
    pattern = rf"(?<![a-z0-9]){escaped_term}(?![a-z0-9])"
    return re.search(pattern, sentence_lower) is not None
