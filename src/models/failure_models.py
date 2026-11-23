
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FailedStep(BaseModel):
    """Details of an individual failed Cucumber step."""

    model_config = ConfigDict(extra="forbid")

    keyword: str
    name: str
    line: int | None = None
    error_message: str


class ScenarioRecord(BaseModel):
    """Standard representation of a Cucumber scenario."""

    model_config = ConfigDict(extra="forbid")

    scenario_id: str
    feature: str
    uri: str
    scenario: str
    line: int | None = None
    tags: list[str] = Field(default_factory=list)
    status: Literal["passed", "failed", "skipped", "unknown"]
    steps_total: int = Field(ge=0)
    steps_failed: int = Field(ge=0)
    failed_steps: list[FailedStep] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_step_counts(self):
        if self.steps_failed != len(self.failed_steps):
            raise ValueError(
                "steps_failed must match the number of failed_steps"
            )

        if self.steps_failed > self.steps_total:
            raise ValueError(
                "steps_failed cannot exceed steps_total"
            )

        if self.status == "failed" and not self.failed_steps:
            raise ValueError(
                "A failed scenario must contain at least one failed step"
            )

        return self


class FailureRecord(ScenarioRecord):
    """A failed scenario with its execution identifier."""

    execution_id: str

    status: Literal["failed"] = "failed"


class ExecutionSummary(BaseModel):
    """Counts for one test execution."""

    model_config = ConfigDict(extra="forbid")

    total_scenarios: int = Field(ge=0)
    passed: int = Field(ge=0)
    failed: int = Field(ge=0)
    skipped: int = Field(ge=0)
    other: int = Field(ge=0)
    total_features: int = Field(ge=0)

    @model_validator(mode="after")
    def validate_total(self):
        counted = self.passed + self.failed + self.skipped + self.other

        if counted != self.total_scenarios:
            raise ValueError(
                "Scenario counts must add up to total_scenarios"
            )

        return self


class ExecutionAnalysis(BaseModel):
    """Complete validated output from the Cucumber parser."""

    model_config = ConfigDict(extra="forbid")

    execution_id: str
    metadata: dict[str, Any]
    summary: ExecutionSummary
    scenarios: list[ScenarioRecord]
    failures: list[FailureRecord]

    @model_validator(mode="after")
    def validate_execution(self):
        if len(self.scenarios) != self.summary.total_scenarios:
            raise ValueError(
                "Scenario list length does not match execution summary"
            )

        if len(self.failures) != self.summary.failed:
            raise ValueError(
                "Failure list length does not match failed count"
            )

        if any(f.execution_id != self.execution_id for f in self.failures):
            raise ValueError(
                "Failure execution IDs must match the execution ID"
            )

        return self

