import json
import os
import requests


# ----------------------------
# Load JSON report safely
# ----------------------------
def load_report(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Report file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# ----------------------------
# Extract test results safely
# ----------------------------
def parse_tests(report):
    tests = report.get("tests", [])

    parsed = []
    for t in tests:
        parsed.append({
            "name": t.get("nodeid", "unknown"),
            "outcome": t.get("outcome", "unknown")
        })

    return parsed


# ----------------------------
# Build Slack message
# ----------------------------
def build_message(tests, title):

    total = len(tests)
    passed = len([t for t in tests if t["outcome"] == "passed"])
    failed = [t["name"] for t in tests if t["outcome"] == "failed"]

    return {
        "text": f"*{title} - Teacher Android Automation*",
        "attachments": [
            {
                "color": "#36a64f" if len(failed) == 0 else "#ff0000",
                "title": "Test Execution Summary",
                "fields": [
                    {"title": "Total Tests", "value": str(total), "short": True},
                    {"title": "Passed", "value": str(passed), "short": True},
                    {"title": "Failed", "value": str(len(failed)), "short": True},
                    {"title": "Failed Test Cases", "value": "\n".join(failed) if failed else "None", "short": False},
                ],
            }
        ],
    }


# ----------------------------
# Send to Slack
# ----------------------------
def send_slack(message):
    webhook = os.getenv("SLACK_WEBHOOK_URL")

    if not webhook:
        raise ValueError("SLACK_WEBHOOK_URL is not set in environment variables")

    response = requests.post(webhook, json=message)

    if response.status_code != 200:
        print("❌ Slack Error:", response.text)
        raise Exception("Slack notification failed")

    print("✅ Slack message sent successfully")


# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":

    report_file = os.getenv("REPORT_FILE")
    title = os.getenv("TITLE", "Automation Tests")

    report = load_report(report_file)
    tests = parse_tests(report)

    message = build_message(tests, title)
    send_slack(message)