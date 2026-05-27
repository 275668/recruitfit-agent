from __future__ import annotations

import pandas as pd
import streamlit as st

from src.interview_generator import generate_interview_questions
from src.jd_parser import parse_jd_requirements
from src.matcher import score_matches
from src.report_builder import build_candidate_report, build_interview_scorecard
from src.resume_evidence import extract_resume_evidence
from src.risk_analyzer import analyze_risks


st.set_page_config(page_title="RecruitFit Agent", layout="wide")

st.title("RecruitFit Agent")
st.caption(
    "Evidence-grounded hiring screening and structured interview preparation. "
    "This MVP does not rewrite resumes or make final hire/reject decisions."
)

with st.sidebar:
    st.header("Inputs")
    job_type = st.selectbox(
        "Job Type",
        ["Product Manager", "AI Product Manager", "Data Analyst", "Software Engineer", "HR Tech", "General"],
    )
    prompt_version = st.selectbox(
        "Prompt Version",
        ["v1_basic", "v2_structured", "v3_evidence_grounded"],
    )
    jd_text = st.text_area(
        "Job Description",
        height=220,
        placeholder="Paste the job description here...",
    )
    resume_text = st.text_area(
        "Candidate Resume",
        height=260,
        placeholder="Paste the candidate resume here...",
    )
    run_analysis = st.button("Run Analysis", type="primary")


def show_table(rows: list[dict]) -> None:
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("No items found.")


if run_analysis:
    if not jd_text.strip() or not resume_text.strip():
        st.warning("Please provide both a job description and a candidate resume before running analysis.")
        st.stop()

    requirements = parse_jd_requirements(jd_text)
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

    st.subheader("Analysis Context")
    st.write(f"Job type: `{job_type}`")
    st.write(f"Prompt version: `{prompt_version}`")

    tabs = st.tabs(
        [
            "JD Skill Decomposition",
            "Resume Evidence Matrix",
            "Match Scoring",
            "Risk Diagnosis",
            "Interview Questions",
            "Interview Scorecard",
            "Final Report",
        ]
    )

    with tabs[0]:
        show_table(requirements)

    with tabs[1]:
        show_table(evidence_items)

    with tabs[2]:
        show_table(match_results)

    with tabs[3]:
        show_table(risk_items)

    with tabs[4]:
        show_table(interview_questions)

    with tabs[5]:
        show_table(scorecard)

    with tabs[6]:
        st.markdown(final_report)
else:
    st.info("Enter a job description and resume in the sidebar, then click Run Analysis.")
