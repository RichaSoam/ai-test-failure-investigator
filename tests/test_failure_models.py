
from pathlib import Path

import pytest
from pydantic import ValidationError

from src.ingestion.cucumber_parser import parse_cucumber_report
from src.models.failure_models import (
    ExecutionAnalysis,
    ExecutionSummary,
    FailureRecord,
)


ROOT = Path(__file__).resolve().parents[1]


def get_parsed_result():
    return parse_cucumber_report(
        ROOT / "test_data" / "sample_cucumber.json",
        ROOT / "test_data" / "execution_metadata.json",
    )


def test_complete_execution_passes_validation():
    parsed = get_parsed_result()

    analysis = ExecutionAnalysis.model_validate(parsed)

    assert analysis.execution_id == "EXEC-001"
    assert analysis.summary.total_scenarios == 100
    assert analysis.summary.passed == 80
    assert analysis.summary.failed == 20
    assert len(analysis.failures) == 20


def test_failure_record_contains_failed_step():
    parsed = get_parsed_result()

    failure = FailureRecord.model_validate(parsed["failures"][0])

    assert failure.status == "failed"
    assert failure.execution_id == "EXEC-001"
    assert len(failure.failed_steps) >= 1
    assert failure.failed_steps[0].error_message


def test_invalid_execution_counts_are_rejected():
    with pytest.raises(ValidationError):
        ExecutionSummary(
            total_scenarios=100,
            passed=80,
            failed=20,
            skipped=5,
            other=0,
            total_features=8,
        )


def test_missing_execution_id_is_rejected():
    parsed = get_parsed_result()["failures"][0].copy()
    parsed.pop("execution_id")

    with pytest.raises(ValidationError):
        FailureRecord.model_validate(parsed)


def test_failed_scenario_without_failed_steps_is_rejected():
    parsed = get_parsed_result()["failures"][0].copy()
    parsed["failed_steps"] = []
    parsed["steps_failed"] = 0

    with pytest.raises(ValidationError):
        FailureRecord.model_validate(parsed)


def test_unexpected_fields_are_rejected():
    parsed = get_parsed_result()["failures"][0].copy()
    parsed["unexpected_field"] = "should not be accepted"

    with pytest.raises(ValidationError):
        FailureRecord.model_validate(parsed)


def test_inconsistent_failure_count_is_rejected():
    parsed = get_parsed_result()
    parsed["summary"]["failed"] = 19

    with pytest.raises(ValidationError):
        ExecutionAnalysis.model_validate(parsed)

