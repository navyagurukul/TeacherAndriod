import pytest
import os
import subprocess
import time
import requests

from appium import webdriver
from appium.options.android import UiAutomator2Options
from utils.config_reader import load_config


# ================= CONFIG =================

@pytest.fixture
def config():
    return load_config()


# ================= WAIT FOR APPIUM =================

def wait_for_appium(server_url, timeout=60):

    status_url = f"{server_url}/status"

    for _ in range(timeout // 5):
        try:
            r = requests.get(status_url, timeout=3)

            if r.status_code == 200:
                print("✅ Appium Server Ready")
                return True

        except Exception:
            time.sleep(5)

    return False


# ================= STOP APP =================

def stop_app(package_name):

    try:

        print(f"🛑 Stopping app: {package_name}")

        subprocess.run(
            ["adb", "shell", "am", "force-stop", package_name],
            check=False,
            timeout=20
        )

        time.sleep(3)

    except Exception as e:

        print(f"⚠ Could not stop app: {e}")


# ================= DRIVER =================

@pytest.fixture(scope="function")
def driver(config):

    server_url = config["appium"]["server_url"]

    if not wait_for_appium(server_url):
        raise Exception("❌ Appium server not running")

    options = UiAutomator2Options()

    # DEVICE
    options.platform_name = config["device"]["platformName"]
    options.device_name = config["device"]["deviceName"]
    options.automation_name = "UiAutomator2"

    # APP
    options.app_package = config["app"]["appPackage"]
    options.app_activity = config["app"]["appActivity"]

    # STABILITY
    options.no_reset = True
    options.full_reset = False
    options.auto_grant_permissions = True

    options.new_command_timeout = 600

    options.set_capability("adbExecTimeout", 120000)
    options.set_capability("uiautomator2ServerLaunchTimeout", 120000)
    options.set_capability("uiautomator2ServerInstallTimeout", 120000)
    options.set_capability("androidInstallTimeout", 120000)

    
    options.set_capability("disableWindowAnimation", True)
    
    print("🚀 Creating Appium Session")

    driver = webdriver.Remote(
        config["appium"]["server_url"],
        options=options
    )

    print("✅ Session Created")
    print(driver.current_package)
    print(driver.session_id)

    yield driver

    try:
        driver.quit()
        print("🛑 Driver Closed")
    except:
        pass


# ================= SCREENSHOT =================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:

        driver = item.funcargs.get("driver")

        if not driver:
            return

        try:

            os.makedirs("screenshots", exist_ok=True)

            file_name = item.name + ".png"

            driver.save_screenshot(
                f"screenshots/{file_name}"
            )

            print(f"📸 Screenshot saved: {file_name}")

        except Exception as e:

            print("❌ Screenshot skipped")
            print(str(e))