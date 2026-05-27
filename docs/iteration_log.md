# Iteration Log

## V0.1 MVP Skeleton

- Created project structure
- Added Streamlit demo shell
- Added placeholder modular workflow
- Added sample data, prompt versions, docs, and output examples

## V0.2 Controlled Rule Improvement

### Iteration Name

Controlled evidence-matching improvement after the first evaluation run.

### Problem Found

The first 10-case evaluation run showed 19 failed checks out of 80 total checks. The main issues were:

- A false positive where a negated sentence, `did not build an AI Agent workflow`, was incorrectly treated as AI Agent evidence.
- False negatives for explicit PRD evidence because resumes used `PRDs` or `product requirements`.
- False negatives for cross-functional communication because resumes used inflected forms such as `communicated`, `collaborated`, and `communication`.
- A Data Analysis miss where the resume used clear phrases such as `growth analysis` and `product dashboards`.

### Changes Made

- Added conservative negation handling so negated skill evidence does not count as positive evidence.
- Added skill-specific PRD variants: `PRDs` and `product requirements`.
- Added skill-specific communication variants: `communication`, `communicated`, `collaborated`, `stakeholders`, and `presented`.
- Added specific Data Analysis variants: `growth analysis`, `dashboards`, and `product dashboards`.
- Avoided broad generic keyword expansion such as `analysis`, `data`, `product`, `project`, `AI`, and `model`.

### Evaluation Result Before And After

| Metric | Before | After |
| --- | ---: | ---: |
| Total cases | 10 | 10 |
| Total checks | 80 | 80 |
| Passed checks | 61 | 78 |
| Failed checks | 19 | 2 |
| Pass rate | 76.25% | 97.50% |

### Remaining Limitations

- `eval_006` still expects Python as a strong skill, but the JD does not explicitly request Python.
- `eval_010` still expects Cross-functional Communication as a strong skill, but the JD does not clearly include a communication requirement.

### Why Remaining Failures Were Intentionally Not Fixed

The remaining failures were not fixed because doing so would require expanding the JD parser beyond explicit JD evidence. That would weaken the product principle that RecruitFit Agent should avoid unsupported inference. The system should not over-expand generic keyword matching just to improve pass rate, because doing so may increase unsupported inference risk.
