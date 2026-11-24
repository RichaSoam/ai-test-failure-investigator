
from pathlib import Path
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from src.classification.groq_classifier import classify_failure
from src.ingestion.cucumber_parser import parse_cucumber_report
from src.models.classification_models import (
    FailureClassification,
)
from src.models.failure_models import FailureRecord


ROOT = Path(__file__).resolve().parents[1]


def get_first_failure():
    parsed = parse_cucumber_report(
        ROOT / "test_data" / "sample_cucumber.json",
        ROOT / "test_data" / "execution_metadata.json",
    )

    return FailureRecord.model_validate(parsed["failures"][0])


class FakeGroqClient:
    """Simulates the Groq response without making an API call."""

    def __init__(self, response_content):
        self.response_content = response_content
        self.chat = SimpleNamespace(
            completions=SimpleNamespace(create=self.create)
        )
        self.call_count = 0

    def create(self, **kwargs):
        self.call_count += 1

        message = SimpleNamespace(content=self.response_content)
        choice = SimpleNamespace(message=message)

        return SimpleNamespace(choices=[choice])


VALID_RESPONSE = """
{
    "category": "locator",
    "confidence": 0.95,
    "likely_cause": "The login button could not be located.",
    "reasoning": "The error message reports that the login button was not found.",
    "evidence": [
        "Watir::Exception::UnknownObjectException",
        "Login button was not found"
    ],
    "recommended_investigation": "Inspect the login button locator and page state.",
    "needs_more_evidence": false
}
"""


def test_valid_classification_is_returned():
    client = FakeGroqClient(VALID_RESPONSE)

    result = classify_failure(
        get_first_failure(),
        client=client,
        model="test-model",
    )

    assert isinstance(result, FailureClassification)
    assert result.category == "locator"
    assert result.confidence == 0.95
    assert len(result.evidence) >= 1


def test_classifier_calls_client_once():
    client = FakeGroqClient(VALID_RESPONSE)

    classify_failure(
        get_first_failure(),
        client=client,
        model="test-model",
    )

    assert client.call_count == 1


def test_invalid_category_is_rejected():
    invalid_response = VALID_RESPONSE.replace(
        '"locator"',
        '"random_category"',
    )

    client = FakeGroqClient(invalid_response)

    with pytest.raises(ValidationError):
        classify_failure(
            get_first_failure(),
            client=client,
            model="test-model",
        )


def test_invalid_json_is_rejected():
    client = FakeGroqClient("This is not JSON")

    with pytest.raises(ValueError, match="invalid JSON"):
        classify_failure(
            get_first_failure(),
            client=client,
            model="test-model",
        )
