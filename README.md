# RecruitFit Agent

## Project Overview

RecruitFit Agent is an AI product prototype for hiring screening and structured interview preparation. It helps HR recruiters, business interviewers, and hiring managers turn a job description and a candidate resume into a structured, evidence-grounded interview preparation report.

The MVP is intentionally rule-based and does not call any external LLM API.

## Product Positioning

RecruitFit Agent is designed to support interview preparation, not to automate hiring decisions. The system focuses on decomposing job requirements, extracting explicit resume evidence, comparing requirements with evidence, diagnosing risks, and generating targeted interview questions.

## Key Features

- Job description skill and requirement decomposition
- Resume evidence extraction
- Evidence-linked match scoring
- Risk and gap diagnosis
- Structured interview question generation
- Interview scorecard preparation
- Final candidate report generation

## Agent Workflow

1. JD Requirement Decomposition
2. Resume Evidence Extraction
3. Evidence-based Match Scoring
4. Risk and Gap Diagnosis
5. Structured Interview Question Generation
6. Interview Scorecard Generation
7. Final Candidate Report Generation

## Product Boundary

RecruitFit Agent is not:

- A resume polishing or rewriting tool
- A final hire or reject decision-maker
- A generic HR comment generator
- A tool for unsupported inference about candidate ability

Every match judgment must be linked to explicit resume evidence. If no evidence is found for a requirement, the system should output: `No evidence found`.

## Demo Preview

The MVP demo is built with Streamlit. Users can paste a job description and candidate resume, select a job type and prompt version, and run a placeholder analysis workflow.

Screenshots will be added in the `screenshots/` folder as the demo evolves.

## Evaluation Design

The evaluation plan focuses on:

- Evidence coverage
- Unsupported inference rate
- Requirement decomposition quality
- Interview question usefulness
- Report clarity and consistency

See `docs/metrics_design.md` for the initial evaluation framework.

## Project Structure

```text
recruitfit-agent/
├── README.md
├── PRD.md
├── app.py
├── requirements.txt
├── data/
├── prompts/
├── src/
├── docs/
├── outputs/
└── screenshots/
```

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Limitations and Future Work

Current limitations:

- Rule-based placeholder logic only
- No external LLM API integration
- Limited sample data
- No robust parsing for complex resumes or job descriptions

Future work:

- Add stronger rule-based extraction
- Add prompt-based and LLM-based reasoning modules
- Expand evaluation cases
- Add exportable reports
- Add bias and compliance review checks
