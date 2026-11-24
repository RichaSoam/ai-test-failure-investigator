import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

from src.classification.groq_classifier import classify_failure
from src.ingestion.cucumber_parser import parse_cucumber_report
from src.models.failure_models import FailureRecord

load_dotenv(ROOT / ".env")

parsed = parse_cucumber_report(
    ROOT / "test_data" / "sample_cucumber.json",
    ROOT / "test_data" / "execution_metadata.json",
)

first_failure = FailureRecord.model_validate(
    parsed["failures"][0]
)

classification = classify_failure(first_failure)

print("\n--- GROQ FAILURE CLASSIFICATION ---")
print(classification.model_dump_json(indent=2))
