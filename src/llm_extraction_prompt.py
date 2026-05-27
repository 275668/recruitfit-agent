from __future__ import annotations

import json


def build_jd_extraction_prompt(jd_text: str) -> str:
    """Build an offline prompt for future LLM-based JD extraction.

    This module does not call an external LLM API. It only prepares an
    auditable prompt that can later be used to replace or assist the current
    rule-based JD parser.
    """
    schema = [
        {
            "skill_name": "string",
            "skill_category": "string",
            "required_keywords": ["string"],
            "importance": "High | Medium | Low",
            "requirement_type": "must_have | preferred | implicit_context",
            "evidence_needed": "string",
        }
    ]

    return f"""You are helping build RecruitFit Agent, an evidence-grounded interview preparation assistant.

Task:
Extract job requirements from the job description into structured JSON.

Rules:
- Output structured JSON only.
- Do not make final hire or reject decisions.
- Do not infer requirements that are not supported by the job description.
- Keep the output auditable by a human reviewer.
- Use concise skill names.
- Use requirement_type to distinguish must-have, preferred, and contextual requirements.
- evidence_needed should describe what explicit resume evidence would be needed to support the requirement.

Required JSON schema:
{json.dumps(schema, indent=2)}

Job description:
\"\"\"{jd_text}\"\"\"
"""


def build_resume_evidence_prompt(resume_text: str, requirements: list[dict]) -> str:
    """Build an offline prompt for future LLM-based resume evidence extraction.

    This prompt is designed to support evidence review, not automatic hiring
    decisions. It requires exact resume evidence and preserves the product
    contract that missing evidence must be reported as "No evidence found".
    """
    schema = [
        {
            "skill_name": "string",
            "resume_evidence": "string",
            "evidence_strength": "Strong | Medium | Missing",
            "matched_text": "string",
            "confidence": 0.0,
            "unsupported_reason": "string",
        }
    ]

    return f"""You are helping build RecruitFit Agent, an evidence-grounded interview preparation assistant.

Task:
For each JD requirement, extract explicit resume evidence from the candidate resume.

Rules:
- Output structured JSON only.
- Do not make final hire or reject decisions.
- Do not infer candidate skills without explicit resume evidence.
- Quote the exact resume evidence when available.
- If no evidence is found, resume_evidence must be exactly: No evidence found
- If no evidence is found, matched_text must be exactly: No evidence found
- Keep the output auditable by a human reviewer.
- evidence_strength must be Strong, Medium, or Missing.
- confidence should be a number from 0.0 to 1.0.
- unsupported_reason should explain missing or weak support without inventing facts.

Required JSON schema:
{json.dumps(schema, indent=2)}

JD requirements:
{json.dumps(requirements, indent=2, ensure_ascii=False)}

Candidate resume:
\"\"\"{resume_text}\"\"\"
"""


def build_evidence_guardrail_prompt(match_results: list[dict]) -> str:
    """Build an offline prompt for auditing evidence-grounded match judgments.

    This guardrail prompt can later be used by an LLM or human reviewer to
    check whether each match is supported by explicit evidence. It does not
    change the current rule-based matcher and does not make hiring decisions.
    """
    schema = [
        {
            "skill_name": "string",
            "original_match_level": "string",
            "is_supported_by_evidence": True,
            "guardrail_decision": "accept | downgrade | needs_human_review",
            "reason": "string",
            "revised_match_level": "Strong Match | Medium Match | Weak Match | No Evidence",
        }
    ]

    return f"""You are auditing RecruitFit Agent match results for evidence grounding.

Task:
Review each match judgment and decide whether it is supported by explicit resume evidence.

Rules:
- Output structured JSON only.
- Do not make final hire or reject decisions.
- Do not infer candidate skills without evidence.
- If resume_evidence is missing, vague, negated, or unsupported, downgrade the match.
- If no evidence is found, revised_match_level should be No Evidence and the reason should mention: No evidence found
- Quote exact evidence when explaining support.
- Keep the output auditable by a human reviewer.

Required JSON schema:
{json.dumps(schema, indent=2)}

Match results to audit:
{json.dumps(match_results, indent=2, ensure_ascii=False)}
"""
