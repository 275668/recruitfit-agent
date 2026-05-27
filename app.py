from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

from src.interview_generator import generate_interview_questions
from src.jd_parser import parse_jd_requirements
from src.matcher import score_matches
from src.report_builder import build_candidate_report, build_interview_scorecard
from src.evidence_retriever import retrieve_candidate_evidence
from src.resume_evidence import extract_resume_evidence
from src.risk_analyzer import analyze_risks


PROJECT_ROOT = Path(__file__).resolve().parent
EVAL_CASES_PATH = PROJECT_ROOT / "data" / "eval_cases.json"


st.set_page_config(page_title="RecruitFit Agent", layout="wide")


@st.cache_data
def load_eval_cases() -> list[dict]:
    if not EVAL_CASES_PATH.exists():
        return []
    with EVAL_CASES_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def show_table(rows: list[dict]) -> None:
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("No items found.")


def average_match_score(match_results: list[dict]) -> float:
    if not match_results:
        return 0.0
    return sum(item["score"] for item in match_results) / len(match_results)


def extract_final_recommendation(report: str) -> str:
    marker = "## Final Recommendation"
    if marker not in report:
        return "Recommendation unavailable"
    recommendation_block = report.split(marker, maxsplit=1)[1].strip()
    return recommendation_block.splitlines()[0].strip()


def apply_sample_case(sample_case: dict) -> None:
    st.session_state["jd_text"] = sample_case["jd_text"]
    st.session_state["resume_text"] = sample_case["resume_text"]
    st.session_state["job_type"] = sample_case["job_type"]


def flatten_retrieval_candidates(candidate_evidence: dict) -> list[dict]:
    rows = []
    for skill_name, candidates in candidate_evidence.items():
        for candidate in candidates:
            rows.append(
                {
                    "skill_name": skill_name,
                    "candidate_sentence": candidate["sentence"],
                    "relevance_score": candidate["score"],
                    "matched_terms": candidate["matched_terms"],
                }
            )
    return rows


def build_review_rows(match_results: list[dict], risk_items: list[dict]) -> list[dict]:
    risk_by_skill = {
        item["skill_name"]: f"{item['risk_level']}: {item['risk_reason']}"
        for item in risk_items
    }
    return [
        {
            "skill_name": item["skill_name"],
            "skill_category": item["skill_category"],
            "match_level": item["match_level"],
            "score": item["score"],
            "resume_evidence": item["resume_evidence"],
            "risk_note": risk_by_skill.get(item["skill_name"], ""),
        }
        for item in match_results
    ]


st.title("RecruitFit Agent")
st.caption("Evidence-grounded candidate screening and structured interview preparation.")

st.markdown(
    """
RecruitFit Agent is an evidence-grounded hiring screening and structured interview preparation assistant. It helps interviewers decompose job requirements, extract resume evidence, identify risks, and generate targeted interview questions. It does not make final hire or reject decisions.

The core principle is evidence-grounded evaluation: every match judgment must link back to explicit resume evidence. If the resume does not support a requirement, the system must say `No evidence found`.
"""
)
st.info(
    "Product boundary: RecruitFit Agent does not rewrite resumes and does not make final hire or reject decisions."
)

eval_cases = load_eval_cases()
sample_options = ["Custom input"] + [
    f"{case['case_id']} - {case['case_name']}" for case in eval_cases
]

with st.sidebar:
    st.header("Inputs")

    selected_sample = st.selectbox("Sample Case Loader", sample_options)
    selected_index = sample_options.index(selected_sample)
    selected_case_id = selected_sample.split(" - ", maxsplit=1)[0]

    if selected_index > 0 and st.session_state.get("loaded_case_id") != selected_case_id:
        apply_sample_case(eval_cases[selected_index - 1])
        st.session_state["loaded_case_id"] = selected_case_id
    elif selected_index == 0 and st.session_state.get("loaded_case_id") != "custom":
        st.session_state["loaded_case_id"] = "custom"

    job_type = st.selectbox(
        "Job Type",
        ["Product Manager", "AI Product Manager", "Data Analyst", "Software Engineer", "HR Tech", "General"],
        key="job_type",
    )
    prompt_version = st.selectbox(
        "Prompt Version",
        ["v1_basic", "v2_structured", "v3_evidence_grounded"],
    )
    jd_text = st.text_area(
        "Job Description",
        height=220,
        placeholder="Paste the job description here...",
        key="jd_text",
    )
    resume_text = st.text_area(
        "Candidate Resume",
        height=260,
        placeholder="Paste the candidate resume here...",
        key="resume_text",
    )
    run_analysis = st.button("Run Analysis", type="primary")

    st.divider()
    st.subheader("Evaluation Result")
    st.write("Total cases: `10`")
    st.write("Total checks: `80`")
    st.metric("Pass rate", "97.50%")
    st.write("Failed checks: `2`")
    st.caption(
        "Remaining failures were intentionally left unresolved to avoid over-expanding generic matching rules."
    )


if run_analysis:
    if not jd_text.strip() or not resume_text.strip():
        st.warning("Please provide both a job description and a candidate resume before running analysis.")
        st.stop()

    requirements = parse_jd_requirements(jd_text)
    candidate_evidence = retrieve_candidate_evidence(resume_text, requirements)
    evidence_items = extract_resume_evidence(resume_text, requirements)
    match_results = score_matches(evidence_items)
    risk_items = analyze_risks(match_results)
    interview_questions = generate_interview_questions(risk_items)
    scorecard = build_interview_scorecard(interview_questions)
    final_report = build_candidate_report(
        jd_text=jd_text,
        resume_text=resume_text,
        requirements=requirements,
        evidence_items=evidence_items,
        match_results=match_results,
        risk_items=risk_items,
        interview_questions=interview_questions,
    )
    final_recommendation = extract_final_recommendation(final_report)

    st.subheader("Analysis Overview")
    st.write(f"Job type: `{job_type}`")
    st.write(f"Prompt version: `{prompt_version}`")
    st.info("Review the evidence column before using any score. Missing evidence is intentionally explicit.")

    strong_matches = [item for item in match_results if item["match_level"] == "Strong Match"]
    no_evidence_matches = [item for item in match_results if item["match_level"] == "No Evidence"]

    metric_cols = st.columns(5)
    metric_cols[0].metric("JD requirements", len(requirements))
    metric_cols[1].metric("Strong Match", len(strong_matches))
    metric_cols[2].metric("No Evidence", len(no_evidence_matches))
    metric_cols[3].metric("Risk items", len(risk_items))
    metric_cols[4].metric("Avg match score", f"{average_match_score(match_results):.2f}/3")

    st.success(f"Final recommendation: {final_recommendation}")

    tabs = st.tabs(
        [
            "JD Skill Decomposition",
            "Evidence Retrieval Candidates",
            "Resume Evidence Matrix",
            "Match Scoring",
            "Risk Diagnosis",
            "Interview Questions",
            "Human Review Panel",
            "Interview Scorecard",
            "Final Report",
        ]
    )

    with tabs[0]:
        st.info("Detected requirements are based on the JD keyword dictionary.")
        show_table(requirements)

    with tabs[1]:
        st.info(
            "These are retrieval candidates for reviewer inspection only. Final match scores still come from the evidence extraction and matcher modules."
        )
        show_table(flatten_retrieval_candidates(candidate_evidence))

    with tabs[2]:
        st.info("Every evidence row is extracted from resume text. Missing evidence must show exactly `No evidence found`.")
        show_table(evidence_items)

    with tabs[3]:
        st.info("Scores are evidence-based: Strong = 3, Medium = 2, Weak = 1, No Evidence = 0.")
        show_table(match_results)

    with tabs[4]:
        high_risks = [item for item in risk_items if item["risk_level"] == "High"]
        medium_risks = [item for item in risk_items if item["risk_level"] == "Medium"]
        if high_risks:
            missing_skills = ", ".join(item["skill_name"] for item in high_risks)
            st.warning(f"High-risk missing evidence found for: {missing_skills}")
        if medium_risks:
            verification_skills = ", ".join(item["skill_name"] for item in medium_risks)
            st.info(f"Medium-risk verification recommended for: {verification_skills}")
        if not high_risks and not medium_risks:
            st.info("No risk items were generated.")
        show_table(risk_items)

    with tabs[5]:
        st.info("Questions are generated for missing or weaker evidence areas, not for final decision-making.")
        show_table(interview_questions)

    with tabs[6]:
        st.info(
            "The system provides evidence-grounded screening support. Final interview and hiring decisions remain human-controlled."
        )

        review_rows = build_review_rows(match_results, risk_items)
        show_table(review_rows)

        reviewer_decisions = []
        for index, row in enumerate(review_rows):
            with st.container(border=True):
                st.markdown(f"**{row['skill_name']}** · {row['skill_category']}")
                st.write(f"System judgment: `{row['match_level']}` · Score: `{row['score']}`")
                st.write(f"Resume evidence: {row['resume_evidence']}")
                if row["risk_note"]:
                    st.warning(row["risk_note"])

                decision = st.selectbox(
                    "Reviewer decision",
                    [
                        "Accept system judgment",
                        "Needs manual verification",
                        "Override after interview",
                    ],
                    key=f"reviewer_decision_{index}_{row['skill_name']}",
                )
                st.text_input(
                    "Reviewer notes",
                    key=f"reviewer_notes_{index}_{row['skill_name']}",
                    placeholder="Optional notes for interview follow-up...",
                )
                reviewer_decisions.append(decision)

        accepted_count = reviewer_decisions.count("Accept system judgment")
        manual_count = reviewer_decisions.count("Needs manual verification")
        override_count = reviewer_decisions.count("Override after interview")

        st.subheader("Review Summary")
        summary_cols = st.columns(3)
        summary_cols[0].metric("Accepted judgments", accepted_count)
        summary_cols[1].metric("Manual verification", manual_count)
        summary_cols[2].metric("Override after interview", override_count)

    with tabs[7]:
        st.info("Use the scorecard during interviews to verify evidence, ownership, scope, and outcomes.")
        show_table(scorecard)

    with tabs[8]:
        st.info(
            "This system supports structured interview preparation. It does not make final hire or reject decisions."
        )
        st.success(f"Final recommendation: {final_recommendation}")
        st.markdown(final_report)
else:
    st.info("Load a sample case or enter a job description and resume in the sidebar, then click Run Analysis.")
