import pytest
import requests
import os
import subprocess

from appium import webdriver
from appium.options.android import UiAutomator2Options
from utils.config_reader import load_config

print("✅ CONFTEST LOADED")


# =========================================================
# CONFIG
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "config.yaml")


@pytest.fixture
def config():
    return load_config()


# =========================================================
# APP STOP HELPER
# =========================================================

def stop_app(package_name):
    subprocess.run(
        f"adb shell am force-stop {package_name}",
        shell=True
    )


# =========================================================
# DRIVER FIXTURE
# =========================================================

@pytest.fixture(scope="function")
def driver(config):

    stop_app(config["app"]["appPackage"])

    options = UiAutomator2Options()

    options.platform_name = config["device"]["platformName"]
    options.device_name = config["device"]["deviceName"]
    options.automation_name = config["device"]["automationName"]

    options.no_reset = False
    options.full_reset = False
    options.auto_grant_permissions = True

    options.app_package = config["app"]["appPackage"]
    options.app_activity = config["app"]["appActivity"]
    options.app_wait_activity = "*"

    driver = webdriver.Remote(
        config["appium"]["server_url"],
        options=options
    )

    yield driver

    driver.quit()


# =========================================================
# GLOBAL TEST RESULTS
# =========================================================

results = []


# =========================================================
# CAPTURE EACH TEST RESULT
# =========================================================

def pytest_runtest_logreport(report):

    if report.when == "call":

        results.append({
            "name": report.nodeid,
            "outcome": report.outcome
        })

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:

        driver = item.funcargs.get("driver")

        if driver:

            os.makedirs("screenshots", exist_ok=True)

            file_name = item.name + ".png"

            driver.save_screenshot(
                f"screenshots/{file_name}"
            )

            print(f"📸 Screenshot saved: {file_name}")

# =========================================================
# FINAL SLACK SUMMARY
# =========================================================

def pytest_sessionfinish(session, exitstatus):

    total = len(results)

    passed = len([
        r for r in results
        if r["outcome"] == "passed"
    ])

    failed = [
        r["name"]
        for r in results
        if r["outcome"] == "failed"
    ]

    title = os.getenv("TITLE", "Automation Tests")

    webhook = os.getenv("SLACK_WEBHOOK_URL")

    message = {
        "text": f"*{title} - Teacher Android Automation*",
        "attachments": [
            {
                "color": "#36a64f" if len(failed) == 0 else "#ff0000",
                "title": "Execution Summary",
                "fields": [
                    {
                        "title": "Total Tests",
                        "value": str(total),
                        "short": True
                    },
                    {
                        "title": "Passed",
                        "value": str(passed),
                        "short": True
                    },
                    {
                        "title": "Failed",
                        "value": str(len(failed)),
                        "short": True
                    },
                    {
                        "title": "Failed Tests",
                        "value": "\n".join(failed) if failed else "None",
                        "short": False
                    },
                ],
            }
        ],
    }

    if webhook:

        response = requests.post(
            webhook,
            json=message
        )

        if response.status_code == 200:
            print("✅ Slack notification sent")
        else:
            print("❌ Slack notification failed")
            print(response.text)
