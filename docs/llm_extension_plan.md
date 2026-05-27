# LLM Extension Plan

## Why The Current MVP Is Rule-based

RecruitFit Agent starts with a rule-based workflow so that the product boundary is clear and the evaluation behavior is explainable. The MVP prioritizes deterministic evidence extraction, transparent keyword rules, and auditable output over broad language generation.

This matters because hiring workflows are sensitive. A screening assistant should not silently infer candidate ability from vague wording or produce final hire or reject decisions.

## How LLM Extraction Could Assist The Workflow

Future versions could use LLM prompts to assist with:

- Extracting JD requirements into structured JSON
- Normalizing skill names and requirement categories
- Extracting exact resume evidence for each requirement
- Explaining why evidence is strong, medium, weak, or missing
- Auditing whether match judgments are supported by explicit evidence

The LLM should operate as an extraction and review assistant, not as an autonomous decision-maker. The output should remain structured, auditable, and tied to exact resume text.

## Embedding-based Retrieval For Evidence Search

The current retrieval layer is deterministic and keyword-based. A future embedding-based retrieval layer could improve evidence search by finding semantically related resume sentences even when exact keywords differ.

Embedding retrieval should still be treated as candidate evidence retrieval only. It should not force a match. Final judgments should require explicit text evidence and should preserve the `No evidence found` behavior when support is absent.

## Human-in-the-loop Review

Human review is important for reducing unsupported inference risk. Recruiters and interviewers should be able to inspect:

- The original JD requirement
- The exact resume evidence
- The match score and explanation
- Any missing or weak evidence
- Suggested interview questions for verification

Human reviewers should be able to downgrade unsupported matches and flag ambiguous evidence before using the report in interview preparation.

## Why Final Hiring Decisions Should Remain Human-controlled

RecruitFit Agent is designed to support structured interview preparation, not to automate hiring outcomes. Final hiring decisions involve context, fairness, legal considerations, team needs, and human judgment that should not be delegated to a prototype screening assistant.

The system should recommend interview preparation actions, not hire or reject decisions.

## Risks If LLM Outputs Are Not Evidence-grounded

If LLM outputs are not evidence-grounded, the system may:

- Infer skills that are not present in the resume
- Convert vague statements into overconfident match judgments
- Hide missing evidence behind polished summaries
- Produce inconsistent or hard-to-audit evaluations
- Introduce bias through unsupported assumptions
- Encourage interviewers to rely on generated claims rather than explicit evidence

To reduce these risks, future LLM modules should require structured JSON, exact evidence quotes, explicit `No evidence found` outputs, and human-reviewable guardrail decisions.
