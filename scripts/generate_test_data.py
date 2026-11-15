
import json
import random
from pathlib import Path
from datetime import datetime, timezone

# Always generate files relative to the project root
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "test_data"
DATA_DIR.mkdir(exist_ok=True)

random.seed(42)

EXECUTION_ID = "EXEC-001"

# Eight features, with 100 scenarios generated across them
FEATURES = {
    "login": {
        "name": "User Login",
        "scenarios": [
            "Login with valid credentials",
            "Login with invalid password",
            "Login with blank username",
            "Login with blank password",
            "Verify account lockout",
            "Login with expired password",
            "Verify remember me",
            "Logout successfully",
            "Login after logout",
            "Verify session timeout",
            "Login with special characters",
            "Verify password masking",
            "Login with inactive account"
        ]
    },
    "customer": {
        "name": "Customer Management",
        "scenarios": [
            "Create a new customer",
            "Update customer details",
            "Search customer by name",
            "Search customer by ID",
            "Delete a customer",
            "Verify mandatory customer fields",
            "Create customer with duplicate email",
            "View customer details",
            "Update customer address",
            "Verify customer status",
            "Export customer details",
            "Filter active customers",
            "Verify customer audit history"
        ]
    },
    "search": {
        "name": "Search",
        "scenarios": [
            "Search product by name",
            "Search product by ID",
            "Search with partial text",
            "Search with no matching result",
            "Search with special characters",
            "Filter search results",
            "Sort search results",
            "Search with blank input",
            "Verify pagination",
            "Search recently added product",
            "Search inactive product",
            "Verify search suggestions",
            "Clear search filters"
        ]
    },
    "orders": {
        "name": "Order Management",
        "scenarios": [
            "Create a new order",
            "View order details",
            "Update order quantity",
            "Cancel an order",
            "Verify order status",
            "Search order by ID",
            "Search orders by date",
            "Verify order history",
            "Export order details",
            "Create order with invalid product",
            "Verify order total",
            "Update delivery address",
            "Verify order confirmation"
        ]
    },
    "payments": {
        "name": "Payments",
        "scenarios": [
            "Make a successful payment",
            "Verify declined payment",
            "Verify payment timeout",
            "View payment history",
            "Refund a payment",
            "Verify payment receipt",
            "Make payment with invalid card",
            "Verify duplicate payment prevention",
            "Verify payment status",
            "Retry a failed payment",
            "Verify payment amount",
            "Cancel payment",
            "Verify payment audit history"
        ]
    },
    "profile": {
        "name": "User Profile",
        "scenarios": [
            "View user profile",
            "Update profile name",
            "Update email address",
            "Change password",
            "Upload profile picture",
            "Verify profile mandatory fields",
            "Update phone number",
            "View user preferences",
            "Update notification settings",
            "Verify profile permissions",
            "Deactivate profile",
            "Reactivate profile",
            "Verify profile audit history"
        ]
    },
    "reports": {
        "name": "Reports",
        "scenarios": [
            "Generate daily report",
            "Generate monthly report",
            "Export report as CSV",
            "Export report as PDF",
            "Filter report by date",
            "Verify report totals",
            "Generate customer report",
            "Generate order report",
            "Generate payment report",
            "Verify report pagination",
            "Schedule a report",
            "Download scheduled report",
            "Verify report permissions"
        ]
    },
    "api": {
        "name": "API Integration",
        "scenarios": [
            "Retrieve customer through API",
            "Create customer through API",
            "Update customer through API",
            "Delete customer through API",
            "Retrieve order through API",
            "Create order through API",
            "Verify invalid API token",
            "Verify API response schema",
            "Verify API response status",
            "Verify API request timeout",
            "Verify API pagination",
            "Verify API error response",
            "Verify API rate limiting"
        ]
    }
}

# Each entry defines a failure known to our test-data generator.
# This information goes ONLY into expected_results.json.
FAILURES = {
    2: {
        "category": "synchronization_issue",
        "group": "SYNC-01",
        "cause": "Page rendering completed after the click attempt",
        "rerun_safe": True,
        "rerun_outcome": "passed",
        "exception": "Watir::Exception::UnknownObjectException",
        "message": "Login button was not found"
    },
    7: {
        "category": "synchronization_issue",
        "group": "SYNC-01",
        "cause": "Page rendering completed after the click attempt",
        "rerun_safe": True,
        "rerun_outcome": "passed",
        "exception": "Watir::Exception::UnknownObjectException",
        "message": "Submit button was not found"
    },
    12: {
        "category": "synchronization_issue",
        "group": "SYNC-02",
        "cause": "AJAX content was not ready when the test interacted with it",
        "rerun_safe": True,
        "rerun_outcome": "passed",
        "exception": "Watir::Wait::TimeoutError",
        "message": "Timed out waiting for search results"
    },
    17: {
        "category": "synchronization_issue",
        "group": "SYNC-02",
        "cause": "AJAX content was not ready when the test interacted with it",
        "rerun_safe": True,
        "rerun_outcome": "passed",
        "exception": "Watir::Wait::TimeoutError",
        "message": "Timed out waiting for order details"
    },
    22: {
        "category": "synchronization_issue",
        "group": "SYNC-02",
        "cause": "AJAX content was not ready when the test interacted with it",
        "rerun_safe": True,
        "rerun_outcome": "passed",
        "exception": "Watir::Wait::TimeoutError",
        "message": "Timed out waiting for report content"
    },
    27: {
        "category": "synchronization_issue",
        "group": "SYNC-02",
        "cause": "AJAX content was not ready when the test interacted with it",
        "rerun_safe": True,
        "rerun_outcome": "passed",
        "exception": "Watir::Wait::TimeoutError",
        "message": "Timed out waiting for profile content"
    },
    32: {
        "category": "api_backend_issue",
        "group": "API-01",
        "cause": "Customer service returned HTTP 503",
        "rerun_safe": True,
        "rerun_outcome": "failed",
        "exception": "Net::HTTPFatalError",
        "message": "503 Service Unavailable"
    },
    37: {
        "category": "api_backend_issue",
        "group": "API-01",
        "cause": "Customer service returned HTTP 503",
        "rerun_safe": True,
        "rerun_outcome": "failed",
        "exception": "RuntimeError",
        "message": "Customer service returned an unsuccessful response"
    },
    42: {
        "category": "api_backend_issue",
        "group": "API-02",
        "cause": "Order service did not respond within the configured timeout",
        "rerun_safe": True,
        "rerun_outcome": "passed",
        "exception": "Net::ReadTimeout",
        "message": "Read timeout while calling order service"
    },
    47: {
        "category": "api_backend_issue",
        "group": "API-02",
        "cause": "Order service did not respond within the configured timeout",
        "rerun_safe": True,
        "rerun_outcome": "passed",
        "exception": "Timeout::Error",
        "message": "Request timed out after 30 seconds"
    },
    52: {
        "category": "locator_issue",
        "group": "LOC-01",
        "cause": "The expected search result locator did not match the page",
        "rerun_safe": False,
        "rerun_outcome": "not_run",
        "exception": "Watir::Exception::UnknownObjectException",
        "message": "Unable to locate search result element"
    },
    57: {
        "category": "locator_issue",
        "group": "LOC-01",
        "cause": "The expected search result locator did not match the page",
        "rerun_safe": False,
        "rerun_outcome": "not_run",
        "exception": "Watir::Exception::UnknownObjectException",
        "message": "Unable to locate product result element"
    },
    62: {
        "category": "locator_issue",
        "group": "LOC-01",
        "cause": "The expected search result locator did not match the page",
        "rerun_safe": False,
        "rerun_outcome": "not_run",
        "exception": "Watir::Exception::UnknownObjectException",
        "message": "Unable to locate filter element"
    },
    67: {
        "category": "environment_issue",
        "group": "ENV-01",
        "cause": "Synthetic QA browser session disconnected",
        "rerun_safe": True,
        "rerun_outcome": "passed",
        "exception": "Selenium::WebDriver::Error::NoSuchDriverError",
        "message": "Browser session is no longer available"
    },
    72: {
        "category": "environment_issue",
        "group": "ENV-01",
        "cause": "Synthetic QA browser session disconnected",
        "rerun_safe": True,
        "rerun_outcome": "passed",
        "exception": "Selenium::WebDriver::Error::WebDriverError",
        "message": "Connection to browser driver was lost"
    },
    77: {
        "category": "environment_issue",
        "group": "ENV-02",
        "cause": "Synthetic QA database connection was unavailable",
        "rerun_safe": True,
        "rerun_outcome": "failed",
        "exception": "OCIError",
        "message": "Database connection could not be established"
    },
    82: {
        "category": "test_data_issue",
        "group": "DATA-01",
        "cause": "Customer record already exists in the test dataset",
        "rerun_safe": False,
        "rerun_outcome": "not_run",
        "exception": "ActiveRecord::RecordNotUnique",
        "message": "Duplicate customer email address"
    },
    87: {
        "category": "test_data_issue",
        "group": "DATA-01",
        "cause": "Customer record already exists in the test dataset",
        "rerun_safe": False,
        "rerun_outcome": "not_run",
        "exception": "RuntimeError",
        "message": "Customer already exists"
    },
    92: {
        "category": "application_defect",
        "group": "APP-01",
        "cause": "Application returned an incorrect order total",
        "rerun_safe": False,
        "rerun_outcome": "not_run",
        "exception": "RSpec::Expectations::ExpectationNotMetError",
        "message": "Expected total 150.0 but received 175.0"
    },
    97: {
        "category": "application_defect",
        "group": "APP-02",
        "cause": "Application returned an incorrect payment status",
        "rerun_safe": False,
        "rerun_outcome": "not_run",
        "exception": "RSpec::Expectations::ExpectationNotMetError",
        "message": "Expected payment status successful but received pending"
    }
}


def ruby_stack_trace(exception, message, feature_file, line):
    """Generate illustrative Ruby/Watir-style stack trace text."""

    return (
        f"{exception}: {message}\n"
        f"\tfrom {feature_file}:{line}:in `block in run_step'\n"
        f"\tfrom /synthetic/project/features/step_definitions/common_steps.rb:42:in `block in click_element'\n"
        f"\tfrom /synthetic/project/vendor/bundle/ruby/gems/watir-7.3.0/lib/watir/elements/element.rb:120:in `click'\n"
        f"\tfrom /synthetic/project/vendor/bundle/ruby/gems/selenium-webdriver-4.20.0/lib/selenium/webdriver/common/element.rb:75:in `click'\n"
    )


def build_scenario(feature_key, feature, scenario_name, index):
    """Create one Cucumber JSON scenario."""

    feature_file = f"features/{feature_key}.feature"
    scenario_line = 10 + (index * 3)
    scenario_id = f"SCN-{index + 1:03d}"

    failure = FAILURES.get(index)

    steps = [
        ("Given ", "user opens the application"),
        ("When ", "user performs the requested action"),
        ("Then ", "expected result should be displayed")
    ]

    step_records = []

    for step_number, (keyword, step_name) in enumerate(steps):
        step_line = scenario_line + step_number + 1

        if failure and step_number == 1:
            error_message = (
                f"{failure['exception']}: {failure['message']}\n"
                + ruby_stack_trace(
                    failure["exception"],
                    failure["message"],
                    feature_file,
                    step_line
                )
            )

            result = {
                "status": "failed",
                "duration": 30000000000,
                "error_message": error_message
            }

        elif failure and step_number == 2:
            result = {
                "status": "skipped"
            }

        else:
            result = {
                "status": "passed",
                "duration": random.randint(300, 2500) * 1000000
            }

        step_records.append({
            "keyword": keyword,
            "name": step_name,
            "line": step_line,
            "result": result
        })

    tags = [
        {"name": "@regression", "line": 1}
    ]

    if index % 5 == 0:
        tags.append({"name": "@smoke", "line": 1})

    if feature_key == "api":
        tags.append({"name": "@api", "line": 1})

    scenario = {
        "id": f"{feature_key};{scenario_id.lower()}",
        "keyword": "Scenario",
        "name": scenario_name,
        "line": scenario_line,
        "type": "scenario",
        "tags": tags,
        "steps": step_records
    }

    expected = None

    if failure:
        expected = {
            "execution_id": EXECUTION_ID,
            "scenario_id": scenario_id,
            "scenario_name": scenario_name,
            "expected_category": failure["category"],
            "expected_group": failure["group"],
            "expected_root_cause": failure["cause"],
            "rerun_safe": failure["rerun_safe"],
            "expected_rerun_outcome": failure["rerun_outcome"]
        }

    return scenario, expected


def generate():
    cucumber_report = []
    expected_results = []

    scenario_index = 0

    for feature_key, feature_info in FEATURES.items():

        elements = []

        for scenario_name in feature_info["scenarios"]:

            if scenario_index >= 100:
                break

            scenario, expected = build_scenario(
                feature_key,
                feature_info,
                scenario_name,
                scenario_index
            )

            elements.append(scenario)

            if expected:
                expected_results.append(expected)

            scenario_index += 1

        cucumber_report.append({
            "id": feature_key,
            "keyword": "Feature",
            "name": feature_info["name"],
            "description": "Synthetic QA automation feature",
            "line": 1,
            "uri": f"features/{feature_key}.feature",
            "elements": elements,
            "tags": [
                {"name": "@regression", "line": 1}
            ]
        })

    report_path = DATA_DIR / "sample_cucumber.json"
    expected_path = DATA_DIR / "expected_results.json"
    metadata_path = DATA_DIR / "execution_metadata.json"

    report_path.write_text(
        json.dumps(cucumber_report, indent=2),
        encoding="utf-8"
    )

    expected_path.write_text(
        json.dumps(expected_results, indent=2),
        encoding="utf-8"
    )

    metadata = {
        "execution_id": EXECUTION_ID,
        "project": "Synthetic QA Automation Project",
        "framework": "Ruby Cucumber + Watir",
        "environment": "QA",
        "branch": "main",
        "build_number": "BUILD-1001",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "total_scenarios": 100,
        "passed_scenarios": 80,
        "failed_scenarios": 20,
        "data_type": "synthetic"
    }

    metadata_path.write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8"
    )

    print("Synthetic Cucumber execution generated.")
    print(f"Total scenarios: {scenario_index}")
    print(f"Passed scenarios: {scenario_index - len(expected_results)}")
    print(f"Failed scenarios: {len(expected_results)}")
    print(f"Report: {report_path}")
    print(f"Expected results: {expected_path}")
    print(f"Metadata: {metadata_path}")


if __name__ == "__main__":
    generate()

