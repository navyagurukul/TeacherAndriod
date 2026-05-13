import pytest
import os
import subprocess
import time
import requests

from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.common.exceptions import WebDriverException

from utils.config_reader import load_config

print("✅ CONFTEST LOADED")


# =========================================================
# CONFIG
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def config():
    return load_config()


# =========================================================
# APP STOP HELPER
# =========================================================

def stop_app(package_name):
    try:
        subprocess.run(
            f"adb shell am force-stop {package_name}",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception:
        pass


# =========================================================
# DRIVER FIXTURE
# =========================================================

@pytest.fixture(scope="function")
def driver(config):

    stop_app(config["app"]["appPackage"])

    options = UiAutomator2Options()

    # Device config
    options.platform_name = config["device"]["platformName"]
    options.device_name = config["device"]["deviceName"]
    options.automation_name = config["device"]["automationName"]

    # App config
    options.app_package = config["app"]["appPackage"]
    options.app_activity = config["app"]["appActivity"]
    options.app_wait_activity = "*"

    # Stability settings (IMPORTANT for CI)
    options.no_reset = False
    options.full_reset = False
    options.auto_grant_permissions = True

    options.new_command_timeout = 600
    options.adb_exec_timeout = 120000
    options.uiautomator2_server_install_timeout = 120000
    options.uiautomator2_server_launch_timeout = 120000

    driver = webdriver.Remote(
        config["appium"]["server_url"],
        options=options
    )

    # IMPORTANT: allow app + UI to stabilize
    time.sleep(6)

    yield driver

    # SAFE TEARDOWN
    try:
        driver.quit()
    except Exception:
        pass


# =========================================================
# GLOBAL RESULTS
# =========================================================

results = []


def pytest_runtest_logreport(report):
    if report.when == "call":
        results.append({
            "name": report.nodeid,
            "outcome": report.outcome
        })


# =========================================================
# SAFE SCREENSHOT HOOK (FIXED CRASH)
# =========================================================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:

        driver = item.funcargs.get("driver")

        if not driver:
            return

        os.makedirs("screenshots", exist_ok=True)
        file_name = item.name + ".png"

        try:
            driver.save_screenshot(f"screenshots/{file_name}")
            print(f"📸 Screenshot saved: {file_name}")

        except WebDriverException:
            print("❌ Screenshot skipped (session already closed)")
        except Exception as e:
            print("❌ Screenshot failed:", str(e))


# =========================================================
# SLACK SUMMARY
# =========================================================

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
                "color": "#36a64f" if not failed else "#ff0000",
                "title": "Execution Summary",
                "fields": [
                    {"title": "Total Tests", "value": str(total), "short": True},
                    {"title": "Passed", "value": str(passed), "short": True},
                    {"title": "Failed", "value": str(len(failed)), "short": True},
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
        try:
            requests.post(webhook, json=message, timeout=10)
            print("✅ Slack notification sent")
        except Exception as e:
            print("❌ Slack notification failed:", str(e))