
import json
from pathlib import Path
from typing import Any


def load_json(file_path: str | Path) -> Any:
    """Load JSON from a file and return its contents."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON in {path}: {exc}"
        ) from exc


def get_tag_names(tags: list) -> list[str]:
    """Support Cucumber tags represented as objects or strings."""
    names = []

    for tag in tags or []:
        if isinstance(tag, dict):
            name = tag.get("name")
            if name:
                names.append(name)
        elif isinstance(tag, str):
            names.append(tag)

    return names


def parse_cucumber_report(
    report_path: str | Path,
    metadata_path: str | Path,
) -> dict:
    """
    Parse a legacy-style Ruby Cucumber JSON report.

    Returns execution metadata, scenario summaries and
    detailed failure records.
    """
    report = load_json(report_path)
    metadata = load_json(metadata_path)

    if not isinstance(report, list):
        raise ValueError(
            "Expected Cucumber JSON report to contain a list of features."
        )

    scenarios = []
    failures = []

    for feature in report:
        if not isinstance(feature, dict):
            continue

        feature_name = feature.get("name", "Unknown feature")
        feature_uri = feature.get("uri", "")

        for scenario in feature.get("elements", []):
            if not isinstance(scenario, dict):
                continue

            steps = scenario.get("steps", [])
            failed_steps = []

            for step in steps:
                result = step.get("result", {})
                if result.get("status") != "failed":
                    continue

                failed_steps.append({
                    "keyword": step.get("keyword", ""),
                    "name": step.get("name", ""),
                    "line": step.get("line"),
                    "error_message": result.get("error_message", ""),
                })

            statuses = [
                step.get("result", {}).get("status", "unknown")
                for step in steps
            ]

            if "failed" in statuses:
                scenario_status = "failed"
            elif statuses and all(s == "passed" for s in statuses):
                scenario_status = "passed"
            elif "skipped" in statuses:
                scenario_status = "skipped"
            else:
                scenario_status = "unknown"

            scenario_record = {
                "scenario_id": scenario.get("id", ""),
                "feature": feature_name,
                "uri": feature_uri,
                "scenario": scenario.get("name", "Unknown scenario"),
                "line": scenario.get("line"),
                "tags": get_tag_names(scenario.get("tags", [])),
                "status": scenario_status,
                "steps_total": len(steps),
                "steps_failed": len(failed_steps),
                "failed_steps": failed_steps,
            }

            scenarios.append(scenario_record)

            if scenario_status == "failed":
                failure_record = {
                    "execution_id": metadata.get(
                        "execution_id", "unknown"
                    ),
                    **scenario_record,
                }
                failures.append(failure_record)

    total = len(scenarios)
    passed = sum(s["status"] == "passed" for s in scenarios)
    failed = sum(s["status"] == "failed" for s in scenarios)
    skipped = sum(s["status"] == "skipped" for s in scenarios)

    return {
        "execution_id": metadata.get("execution_id", "unknown"),
        "metadata": metadata,
        "summary": {
            "total_scenarios": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "other": total - passed - failed - skipped,
            "total_features": len(report),
        },
        "scenarios": scenarios,
        "failures": failures,
    }