# Error Analysis

## Current Evaluation Summary

- total_cases: 10
- total_checks: 80
- passed_checks: 61
- failed_checks: 19
- pass_rate: 76.25%

## Failure Categories

### False Positive: Expected Missing Skill Was Incorrectly Matched

| case_id | case_name | skill_name | expected result | actual result | likely cause |
| --- | --- | --- | --- | --- | --- |
| eval_008 | CADD AIDD background transitioning to AI product | AI Agent | No Evidence with `resume_evidence` exactly `No evidence found` | Strong Match; evidence: "Explored LLM summaries for experiment notes but did not build an AI Agent workflow." | The matcher detects `AI Agent workflow` inside a negated sentence. The current rule-based extraction does not handle negation such as "did not build". |

### False Negative: Expected Strong Skill Was Not Detected Or Marked No Evidence

| case_id | case_name | skill_name | expected result | actual result | likely cause |
| --- | --- | --- | --- | --- | --- |
| eval_001 | Strong AI Product Manager match | Product Requirement Document | Strong Match or Medium Match | No Evidence; evidence: `No evidence found` | Resume uses `PRDs`, but the evidence keyword list includes `prd` and not the plural form `prds`. |
| eval_001 | Strong AI Product Manager match | Cross-functional Communication | Strong Match or Medium Match | No Evidence; evidence: `No evidence found` | Resume says `communicated` and `engineering stakeholders`; current keywords include `communicate` and `stakeholder`, but matching is exact substring and does not cover inflections reliably. |
| eval_002 | Medium product candidate with weak AI evidence | Product Requirement Document | Strong Match or Medium Match | No Evidence; evidence: `No evidence found` | Resume uses `PRDs`; plural acronym is not covered. |
| eval_004 | Candidate missing SQL evidence | Product Requirement Document | Strong Match or Medium Match | No Evidence; evidence: `No evidence found` | Resume uses `PRDs`; plural acronym is not covered. |
| eval_005 | Candidate missing A/B testing evidence | Data Analysis | Strong Match or Medium Match | No Evidence; evidence: `No evidence found` | Resume says `growth analysis`, `SQL`, and `product dashboards`; current Data Analysis keywords do not include `analysis` by itself or product analytics phrasing. |
| eval_005 | Candidate missing A/B testing evidence | Product Requirement Document | Strong Match or Medium Match | No Evidence; evidence: `No evidence found` | Resume uses `PRDs`; plural acronym is not covered. |
| eval_005 | Candidate missing A/B testing evidence | Cross-functional Communication | Strong Match or Medium Match | No Evidence; evidence: `No evidence found` | Resume says `communicated findings to design and engineering`; current evidence matching does not cover `communicated`. |
| eval_006 | AI project without PRD or user story evidence | Cross-functional Communication | Strong Match or Medium Match | No Evidence; evidence: `No evidence found` | Resume says `Presented technical findings to engineers`; this is a communication signal, but it does not match the current communication keywords. |
| eval_007 | Product experience without AI Agent workflow evidence | Product Requirement Document | Strong Match or Medium Match | No Evidence; evidence: `No evidence found` | Resume uses `PRDs`; plural acronym is not covered. |
| eval_007 | Product experience without AI Agent workflow evidence | Cross-functional Communication | Strong Match or Medium Match | No Evidence; evidence: `No evidence found` | Resume says `collaborated with engineering, sales, and customer success`; current keyword list has `collaborate`, not `collaborated`. |
| eval_008 | CADD AIDD background transitioning to AI product | Product Requirement Document | Strong Match or Medium Match | No Evidence; evidence: `No evidence found` | Resume says `product requirements`; current PRD keywords include `product requirement` singular but evidence may need better phrase handling or plural coverage. |
| eval_009 | HR Tech screening scenario | Product Requirement Document | Strong Match or Medium Match | No Evidence; evidence: `No evidence found` | Resume uses `PRDs`; plural acronym is not covered. |
| eval_009 | HR Tech screening scenario | Cross-functional Communication | Strong Match or Medium Match | No Evidence; evidence: `No evidence found` | Resume says `Collaborated with HR, legal, and engineering stakeholders`; current matching misses `Collaborated` due to inflection. |

### JD Parsing Miss: Expected Skill Was Not Detected From The JD

| case_id | case_name | skill_name | expected result | actual result | likely cause |
| --- | --- | --- | --- | --- | --- |
| eval_002 | Medium product candidate with weak AI evidence | Cross-functional Communication | Strong Match or Medium Match | Skill not detected from JD | JD says `close communication with engineering`; current JD parser keywords do not include `communication`. |
| eval_003 | Buzzwords with weak project evidence | Cross-functional Communication | Strong Match or Medium Match | Skill not detected from JD | JD says `product communication experience`; current JD parser looks for `communicate`, not `communication`. |
| eval_006 | AI project without PRD or user story evidence | Python | Strong Match or Medium Match | Skill not detected from JD | JD does not explicitly mention Python, so this may be an eval-case expectation issue rather than a parser bug. |
| eval_008 | CADD AIDD background transitioning to AI product | Cross-functional Communication | Strong Match or Medium Match | Skill not detected from JD | JD says `communication with scientists and engineers`; current JD parser does not include `communication`. |
| eval_010 | Unsupported inference stress test | Cross-functional Communication | Strong Match or Medium Match | Skill not detected from JD | JD does not clearly request communication; the expected strong skill may be inconsistent with the JD. |

### Evidence Formatting Issue: Resume Evidence Was Not Exactly `No evidence found`

No standalone evidence formatting issues were found. The only missing-skill exact-format violation is the eval_008 AI Agent false positive, where the system returned a matched sentence instead of `No evidence found`.

### Other

No failures currently require an `Other` category. The observed failures fit false positive, false negative, or JD parsing miss patterns.

## Pattern Notes

- PRD evidence is repeatedly missed because resumes often use `PRDs`, while the current dictionary mainly expects `prd`.
- Communication evidence is repeatedly missed because the workflow relies on exact keyword substrings and misses inflections such as `communicated`, `collaborated`, and noun forms such as `communication`.
- One high-priority false positive appears when a negated sentence contains an otherwise strong phrase: `did not build an AI Agent workflow`.
- Some evaluation expectations may need review when the JD does not explicitly contain the expected skill, especially Python in eval_006 and Cross-functional Communication in eval_010.

## Priority Fix Plan

1. Fix false positives for expected missing skills.
   - Add basic negation handling around strong skill phrases, especially for AI Agent patterns such as `did not build`, `no experience`, or `without`.
   - Ensure negated evidence does not produce Strong Match, Medium Match, or Weak Match.

2. Fix important false negatives for core skills such as AI Agent, Workflow Design, PRD, SQL, A/B Testing, Evaluation Metrics.
   - Add carefully scoped variants such as `PRDs`, `product requirements`, `communicated`, and `collaborated`.
   - Prefer skill-specific phrase variants over broad generic words.

3. Improve JD parser coverage only when the JD clearly contains the skill.
   - Add `communication` as a Cross-functional Communication trigger.
   - Review eval expectations where the JD does not clearly contain the skill before expanding parser coverage.

4. Avoid over-expanding generic keywords that may increase hallucination risk.
   - Do not treat broad terms like `AI`, `product`, `roadmap`, or `strategy` as evidence for specialized skills.
   - Keep the evidence-grounded boundary: if explicit resume evidence is absent, output exactly `No evidence found`.
