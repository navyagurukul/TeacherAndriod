import pytest
import os
import subprocess
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from utils.config_reader import load_config

print("✅ CONFTEST LOADED")


# ================= CONFIG =================

@pytest.fixture
def config():
    return load_config()


# ================= STOP APP =================

def stop_app(package_name):
    try:
        subprocess.run(
            f"adb shell am force-stop {package_name}",
            shell=True,
            timeout=10
        )
    except:
        pass


# ================= DRIVER =================

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

    # IMPORTANT STABILITY SETTINGS
    options.new_command_timeout = 600

    options.set_capability("adbExecTimeout", 120000)
    options.set_capability("uiautomator2ServerLaunchTimeout", 120000)
    options.set_capability("uiautomator2ServerInstallTimeout", 120000)

    options.app_package = config["app"]["appPackage"]
    options.app_activity = config["app"]["appActivity"]
    options.app_wait_activity = "*"

    driver = None

    try:
        driver = webdriver.Remote(
            config["appium"]["server_url"],
            options=options
        )

        # 🔥 IMPORTANT: wait for session stabilization
        time.sleep(8)

        yield driver

    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass


# ================= SAFE SCREENSHOT =================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:

        driver = item.funcargs.get("driver", None)

        if not driver:
            return

        try:
            os.makedirs("screenshots", exist_ok=True)
            file_name = item.name + ".png"
            driver.save_screenshot(f"screenshots/{file_name}")
            print(f"📸 Screenshot saved: {file_name}")

        except Exception as e:
            print("❌ Screenshot skipped (session already closed)")
            print(str(e))