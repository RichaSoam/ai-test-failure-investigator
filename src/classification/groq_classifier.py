
import json
import os

from groq import Groq

from src.models.classification_models import FailureClassification


SYSTEM_PROMPT = """
You are an experienced QA automation failure investigator.

Analyse one failed scenario from a Ruby Cucumber and Watir test execution.

Classify the failure into exactly one category:

- synchronization: timing, waiting, asynchronous loading,
  stale state or transient UI readiness
- api_backend: API request, HTTP response, service,
  database connectivity or backend processing
- locator: missing or incorrect element locator,
  element not found or ambiguous element selection
- environment: browser, driver, network, infrastructure,
  unavailable service or execution environment
- test_data: missing, invalid, duplicated or inconsistent test data
- application_defect: evidence of incorrect application behaviour
- unknown: insufficient evidence to make a reasonable classification

Important rules:

1. Use only evidence present in the supplied failure record.
2. Do not invent logs, application behaviour or root causes.
3. A stack trace is evidence, but an exception name alone
   does not always prove the root cause.
4. Distinguish observed facts from hypotheses.
5. If evidence is insufficient, choose unknown or set
   needs_more_evidence to true.
6. Do not recommend a test rerun or claim that a defect is confirmed.
7. Include short, specific evidence snippets from the input.

Return a JSON object with these fields:
category, confidence, likely_cause, reasoning, evidence,
recommended_investigation, needs_more_evidence.

Confidence must be between 0 and 1.
"""


def classify_failure(failure, client=None, model=None):
    """
    Classify one validated FailureRecord using Groq.

    The client and model can be injected for testing.
    """

    api_key = os.getenv("GROQ_API_KEY")
    selected_model = model or os.getenv("GROQ_MODEL")

    if client is None:
        if not api_key:
            raise ValueError("GROQ_API_KEY is not configured.")

        client = Groq(api_key=api_key)

    if not selected_model:
        raise ValueError("GROQ_MODEL is not configured.")

    failure_data = failure.model_dump()

    response = client.chat.completions.create(
        model=selected_model,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": json.dumps(failure_data, indent=2),
            },
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("Groq returned an empty classification response.")

    try:
        result = json.loads(content)
    except json.JSONDecodeError as exc:
        raise ValueError(
            "Groq returned invalid JSON."
        ) from exc

    return FailureClassification.model_validate(result)
