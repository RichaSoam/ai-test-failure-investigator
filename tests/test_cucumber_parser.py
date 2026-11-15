
from pathlib import Path

from src.ingestion.cucumber_parser import parse_cucumber_report


ROOT = Path(__file__).resolve().parents[1]

REPORT = ROOT / "test_data" / "sample_cucumber.json"
METADATA = ROOT / "test_data" / "execution_metadata.json"


def get_result():
    return parse_cucumber_report(REPORT, METADATA)


def test_report_has_100_scenarios():
    result = get_result()

    assert result["summary"]["total_scenarios"] == 100


def test_report_has_80_passed_scenarios():
    result = get_result()

    assert result["summary"]["passed"] == 80


def test_report_has_20_failed_scenarios():
    result = get_result()

    assert result["summary"]["failed"] == 20
    assert len(result["failures"]) == 20


def test_report_has_8_features():
    result = get_result()

    assert result["summary"]["total_features"] == 8


def test_every_failure_has_detailed_error_information():
    result = get_result()

    for failure in result["failures"]:
        assert failure["execution_id"]
        assert failure["feature"]
        assert failure["scenario"]
        assert failure["uri"]
        assert failure["failed_steps"]

        for step in failure["failed_steps"]:
            assert step["name"]
            assert step["error_message"]


def test_parser_does_not_include_ground_truth():
    result = get_result()

    assert "expected_results" not in result
    assert all(
        "expected_category" not in failure
        for failure in result["failures"]
    )