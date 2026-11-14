import json
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.environ["GROQ_API_KEY"]
)

MODEL = os.environ["GROQ_MODEL"]


def investigate_failure(failure):

    prompt = f"""
You are an AI Test Failure Investigator.

Analyse the following synthetic test failure.

Failure information:
{json.dumps(failure, indent=2)}

Classify the failure into one of these categories:
- application_defect
- locator_issue
- synchronization_issue
- environment_issue
- test_data_issue
- unknown

Return:
1. Failure category
2. Likely cause
3. Supporting evidence
4. Recommended investigation
5. Confidence from 0 to 100

Rules:
- Separate observed evidence from hypotheses.
- Do not invent evidence.
- Do not claim a root cause is proven without sufficient evidence.
- If evidence is insufficient, say so.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a careful QA automation investigator."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    with open(
        "test_data/synthetic_failures.json",
        "r"
    ) as file:
        failures = json.load(file)

    for failure in failures:
        print("\n" + "=" * 60)
        print("Failure ID:", failure["id"])
        print(investigate_failure(failure))
