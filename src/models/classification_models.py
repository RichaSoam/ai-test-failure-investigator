
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


FailureCategory = Literal[
    "synchronization",
    "api_backend",
    "locator",
    "environment",
    "test_data",
    "application_defect",
    "unknown",
]


class FailureClassification(BaseModel):
    """Structured AI classification of a test failure."""

    model_config = ConfigDict(extra="forbid")

    category: FailureCategory

    confidence: float = Field(ge=0.0, le=1.0)

    likely_cause: str

    reasoning: str

    evidence: list[str] = Field(min_length=1)

    recommended_investigation: str

    needs_more_evidence: bool