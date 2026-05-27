# Product Requirements Document: RecruitFit Agent

## 1. Purpose

RecruitFit Agent helps interviewers prepare structured, evidence-grounded candidate evaluations from a job description and a candidate resume.

## 2. Target Users

- HR recruiters
- Business interviewers
- Hiring managers

## 3. Core Problem

Interviewers often need to quickly understand whether a candidate has explicit evidence for key job requirements. Generic resume summaries are not enough; interviewers need traceable evidence, gaps, risks, and targeted questions.

## 4. MVP Scope

The MVP provides a Streamlit demo with placeholder rule-based workflow stages:

1. JD Requirement Decomposition
2. Resume Evidence Extraction
3. Evidence-based Match Scoring
4. Risk and Gap Diagnosis
5. Structured Interview Question Generation
6. Interview Scorecard Generation
7. Final Candidate Report Generation

## 5. Non-goals

- Do not rewrite resumes
- Do not make final hire or reject decisions
- Do not infer abilities from vague wording
- Do not call external LLM APIs in the initial MVP

## 6. Evidence-grounded Principle

Every match judgment must be linked to explicit resume evidence. If no evidence is found, the system must clearly output `No evidence found`.

## 7. Success Criteria

- The demo runs locally
- The workflow is modular and readable
- Output sections map clearly to the agent workflow
- The product boundary is clear in docs and UI
