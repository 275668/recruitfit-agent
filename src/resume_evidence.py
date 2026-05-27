from __future__ import annotations

import re


HIGHLY_SPECIFIC_KEYWORDS = {
    "prd",
    "prds",
    "product requirement",
    "product requirements",
    "requirements document",
    "user story",
    "acceptance criteria",
    "figma",
    "ai agent",
    "agent system",
    "agent workflow",
    "agentic",
    "ticket agent",
    "autonomous agent",
    "large language model",
    "prompt engineering",
    "retrieval augmented generation",
    "streamlit",
    "sql",
    "a/b testing",
    "ab testing",
    "evaluation metric",
    "success metric",
    "hr tech",
    "talent acquisition",
}

AGENT_CONTEXT_KEYWORDS = {"workflow", "classification", "escalation"}


def extract_resume_evidence(resume_text: str, requirements: list[dict]) -> list[dict]:
    """Find explicit resume evidence for each JD requirement."""
    sentences = _split_sentences(resume_text)
    evidence_items = []

    for requirement in requirements:
        matched_sentences = []
        matched_keywords = []

        for sentence in sentences:
            sentence_lower = sentence.lower()
            sentence_matches = _find_keyword_matches(
                sentence_lower,
                requirement["required_keywords"],
            )
            if sentence_matches:
                matched_sentences.append(sentence)
                matched_keywords.extend(sentence_matches)

        unique_keywords = sorted(set(matched_keywords))
        resume_evidence = " ".join(matched_sentences[:2]) if matched_sentences else "No evidence found"

        evidence_items.append(
            {
                "skill_name": requirement["skill_name"],
                "skill_category": requirement["skill_category"],
                "resume_evidence": resume_evidence,
                "matched_keywords": unique_keywords,
                "evidence_strength": _classify_evidence_strength(
                    unique_keywords,
                    matched_sentences,
                    requirement["skill_name"],
                ),
            }
        )

    return evidence_items


def _split_sentences(text: str) -> list[str]:
    cleaned_text = re.sub(r"\s+", " ", text.strip())
    if not cleaned_text:
        return []
    return [
        sentence.strip(" -")
        for sentence in re.split(r"(?<=[.!?])\s+|\n+", cleaned_text)
        if sentence.strip(" -")
    ]


def _find_keyword_matches(sentence_lower: str, keywords: list[str]) -> list[str]:
    matches = []

    for keyword in sorted(keywords, key=len, reverse=True):
        if _contains_keyword(sentence_lower, keyword) and not _is_negated_match(
            sentence_lower,
            keyword,
        ):
            matches.append(keyword)

    return matches


def _contains_keyword(sentence_lower: str, keyword: str) -> bool:
    escaped_keyword = re.escape(keyword.lower())
    pattern = rf"(?<![a-z0-9]){escaped_keyword}(?![a-z0-9])"
    return re.search(pattern, sentence_lower) is not None


def _is_negated_match(sentence_lower: str, keyword: str) -> bool:
    escaped_keyword = re.escape(keyword.lower())
    optional_words = r"(?:\s+\w+){0,3}\s+"
    negation_patterns = [
        rf"\bdid\s+not{optional_words}{escaped_keyword}\b",
        rf"\bdoes\s+not{optional_words}{escaped_keyword}\b",
        rf"\bdo\s+not{optional_words}{escaped_keyword}\b",
        rf"\bnot{optional_words}{escaped_keyword}\b",
        rf"\bwithout{optional_words}{escaped_keyword}\b",
        rf"\bno{optional_words}{escaped_keyword}\b",
    ]
    return any(re.search(pattern, sentence_lower) for pattern in negation_patterns)


def _classify_evidence_strength(
    matched_keywords: list[str],
    matched_sentences: list[str],
    skill_name: str,
) -> str:
    if not matched_keywords:
        return "Missing"

    if any(keyword in HIGHLY_SPECIFIC_KEYWORDS for keyword in matched_keywords):
        return "Strong"

    if skill_name == "AI Agent" and matched_keywords == ["agent"]:
        combined_evidence = " ".join(matched_sentences).lower()
        if any(keyword in combined_evidence for keyword in AGENT_CONTEXT_KEYWORDS):
            return "Strong"
        return "Medium"

    if len(matched_keywords) >= 2:
        return "Strong"

    return "Medium"
