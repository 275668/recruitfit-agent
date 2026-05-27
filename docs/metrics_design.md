# Metrics Design

## Goal

Evaluate whether RecruitFit Agent produces useful, evidence-grounded interview preparation outputs.

## Initial Metrics

- Evidence coverage
- Unsupported inference rate
- Requirement decomposition quality
- Question relevance
- Report clarity

## Current Evaluation Metrics

The current evaluation set contains 10 cases and 80 total checks.

| Metric | Value |
| --- | ---: |
| Total cases | 10 |
| Total checks | 80 |
| Passed checks | 78 |
| Failed checks | 2 |
| Pass rate | 97.50% |

### Expected Strong Skill Check

For each skill listed in `expected_strong_skills`, the check passes if the workflow returns either:

- `Strong Match`
- `Medium Match`

The check fails if the workflow returns:

- `Weak Match`
- `No Evidence`
- skill not detected from the JD

### Expected Missing Skill Check

For each skill listed in `expected_missing_skills`, the check passes only if:

- `match_level` is `No Evidence`
- `resume_evidence` is exactly `No evidence found`

The check fails if:

- the skill is matched as `Strong Match`, `Medium Match`, or `Weak Match`
- `resume_evidence` is not exactly `No evidence found`
- the skill is not detected from the JD

### No Evidence Found Exact-match Check

The exact phrase `No evidence found` is treated as a product-level contract. It ensures that missing evidence is explicit, parseable, and easy for interviewers to review. This also prevents the system from hiding missing evidence behind vague language.

## Evaluation Principle

The evaluation should reward evidence-grounded behavior, not keyword overfitting. RecruitFit Agent should not over-expand generic keyword matching just to improve pass rate, because doing so may increase unsupported inference risk.

Future keyword changes should be skill-specific and traceable to explicit JD or resume wording. Broad terms such as `analysis`, `data`, `product`, `project`, `AI`, and `model` should be used carefully because they can create false positives.

## MVP Notes

The first version uses rule-based placeholder logic, so metrics are design targets rather than production benchmarks.
