import pytest
import requests
import os

# ----------------------------
# GLOBAL STORAGE (in-memory)
# ----------------------------
results = []


# ----------------------------
# CAPTURE EACH TEST RESULT
# ----------------------------
def pytest_runtest_logreport(report):
    if report.when == "call":
        results.append({
            "name": report.nodeid,
            "outcome": report.outcome
        })


# ----------------------------
# FINAL SUMMARY AFTER ALL TESTS
# ----------------------------
def pytest_sessionfinish(session, exitstatus):

    total = len(results)
    passed = len([r for r in results if r["outcome"] == "passed"])
    failed = [r["name"] for r in results if r["outcome"] == "failed"]

    title = os.getenv("TITLE", "Automation Tests")
    webhook = os.getenv("SLACK_WEBHOOK_URL")

    message = {
        "text": f"*{title} - Teacher Android Automation*",
        "attachments": [
            {
                "color": "#36a64f" if len(failed) == 0 else "#ff0000",
                "fields": [
                    {"title": "Total Tests", "value": str(total), "short": True},
                    {"title": "Passed", "value": str(passed), "short": True},
                    {"title": "Failed", "value": str(len(failed)), "short": True},
                    {"title": "Failed Tests", "value": "\n".join(failed) if failed else "None", "short": False},
                ],
            }
        ],
    }

    if webhook:
        requests.post(webhook, json=message)