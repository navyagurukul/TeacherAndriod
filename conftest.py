import pytest
import os
import yaml
from appium import webdriver
from appium.options.android import UiAutomator2Options
from utils.config_reader import load_config

# ================= CONFIG =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "config.yaml")

@pytest.fixture
def config():
    return load_config()

# ================= DRIVER =================
@pytest.fixture(scope="function")
def driver(config):

    import subprocess
    subprocess.run(
        "adb shell am force-stop com.OritSciencesPrivateLimited.EnglishGurukul.teacher",
        shell=True
    )

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