from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
DATA_PATH = PROJECT_ROOT / "data" / "eval_cases.json"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "eval_results.json"

sys.path.insert(0, str(PROJECT_ROOT))

from src.interview_generator import generate_interview_questions
from src.jd_parser import parse_jd_requirements
from src.matcher import score_matches
from src.resume_evidence import extract_resume_evidence
from src.risk_analyzer import analyze_risks


PASSING_STRONG_LEVELS = {"Strong Match", "Medium Match"}


def main() -> None:
    eval_cases = load_eval_cases()
    detailed_results = []

    total_checks = 0
    passed_checks = 0

    for case in eval_cases:
        result = evaluate_case(case)
        detailed_results.append(result)

        total_checks += result["passed_checks"] + result["failed_checks"]
        passed_checks += result["passed_checks"]

        print_case_summary(result)

    failed_checks = total_checks - passed_checks
    pass_rate = passed_checks / total_checks if total_checks else 0

    overall_summary = {
        "total_cases": len(eval_cases),
        "total_checks": total_checks,
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "pass_rate": round(pass_rate, 4),
    }

    print_overall_summary(overall_summary)
    save_results(overall_summary, detailed_results)


def load_eval_cases() -> list[dict]:
    with DATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_case(case: dict) -> dict:
    requirements = parse_jd_requirements(case["jd_text"])
    evidence_items = extract_resume_evidence(case["resume_text"], requirements)
    match_results = score_matches(evidence_items)
    risk_items = analyze_risks(match_results)
    interview_questions = generate_interview_questions(risk_items)

    match_by_skill = {item["skill_name"]: item for item in match_results}
    failure_details = []
    check_details = []

    for skill_name in case.get("expected_strong_skills", []):
        check = check_expected_strong(skill_name, match_by_skill)
        check_details.append(check)
        if not check["passed"]:
            failure_details.append(check["failure_detail"])

    for skill_name in case.get("expected_missing_skills", []):
        check = check_expected_missing(skill_name, match_by_skill)
        check_details.append(check)
        if not check["passed"]:
            failure_details.append(check["failure_detail"])

    passed_checks = sum(1 for check in check_details if check["passed"])
    failed_checks = len(check_details) - passed_checks

    return {
        "case_id": case["case_id"],
        "case_name": case["case_name"],
        "job_type": case["job_type"],
        "passed_checks": passed_checks,
        "failed_checks": failed_checks,
        "failure_details": failure_details,
        "check_details": check_details,
        "actual_requirements": requirements,
        "actual_evidence_items": evidence_items,
        "actual_match_results": match_results,
        "actual_risk_items": risk_items,
        "actual_interview_questions": interview_questions,
    }


def check_expected_strong(skill_name: str, match_by_skill: dict[str, dict]) -> dict:
    actual = match_by_skill.get(skill_name)

    if actual is None:
        return build_check_result(
            skill_name=skill_name,
            expectation="expected_strong",
            passed=False,
            actual_match_level="Skill not detected",
            actual_resume_evidence="No evidence found",
            failure_detail=f"{skill_name}: expected Strong/Medium Match, but skill was not detected from the JD.",
        )

    match_level = actual["match_level"]
    passed = match_level in PASSING_STRONG_LEVELS

    return build_check_result(
        skill_name=skill_name,
        expectation="expected_strong",
        passed=passed,
        actual_match_level=match_level,
        actual_resume_evidence=actual["resume_evidence"],
        failure_detail=(
            ""
            if passed
            else f"{skill_name}: expected Strong/Medium Match, got {match_level}."
        ),
    )


def check_expected_missing(skill_name: str, match_by_skill: dict[str, dict]) -> dict:
    actual = match_by_skill.get(skill_name)

    if actual is None:
        return build_check_result(
            skill_name=skill_name,
            expectation="expected_missing",
            passed=False,
            actual_match_level="Skill not detected",
            actual_resume_evidence="No evidence found",
            failure_detail=f"{skill_name}: expected No Evidence, but skill was not detected from the JD.",
        )

    match_level = actual["match_level"]
    resume_evidence = actual["resume_evidence"]
    passed = match_level == "No Evidence" and resume_evidence == "No evidence found"

    return build_check_result(
        skill_name=skill_name,
        expectation="expected_missing",
        passed=passed,
        actual_match_level=match_level,
        actual_resume_evidence=resume_evidence,
        failure_detail=(
            ""
            if passed
            else (
                f"{skill_name}: expected No Evidence with exact resume evidence "
                f"'No evidence found', got {match_level} with evidence '{resume_evidence}'."
            )
        ),
    )


def build_check_result(
    skill_name: str,
    expectation: str,
    passed: bool,
    actual_match_level: str,
    actual_resume_evidence: str,
    failure_detail: str,
) -> dict:
    return {
        "skill_name": skill_name,
        "expectation": expectation,
        "passed": passed,
        "actual_match_level": actual_match_level,
        "actual_resume_evidence": actual_resume_evidence,
        "failure_detail": failure_detail,
    }


def print_case_summary(result: dict) -> None:
    print("=" * 80)
    print(f"{result['case_id']} - {result['case_name']}")
    print(f"Passed checks: {result['passed_checks']}")
    print(f"Failed checks: {result['failed_checks']}")

    if result["failure_details"]:
        print("Failure details:")
        for detail in result["failure_details"]:
            print(f"- {detail}")
    else:
        print("Failure details: None")


def print_overall_summary(summary: dict) -> None:
    print("=" * 80)
    print("Overall Summary")
    print(f"total_cases: {summary['total_cases']}")
    print(f"total_checks: {summary['total_checks']}")
    print(f"passed_checks: {summary['passed_checks']}")
    print(f"failed_checks: {summary['failed_checks']}")
    print(f"pass_rate: {summary['pass_rate']:.2%}")


def save_results(overall_summary: dict, case_results: list[dict]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "overall_summary": overall_summary,
        "case_results": case_results,
    }
    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)

    print(f"Saved detailed results to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
