from appium import webdriver
from appium.options.android import UiAutomator2Options


class AppiumDriver:

    def __init__(self, config):

        self.config = config
        self.driver = None

    def start_driver(self):

        print("🚀 Starting Appium Driver")

        options = UiAutomator2Options()

        # DEVICE CONFIG
        options.platform_name = self.config["device"]["platformName"]
        options.device_name = self.config["device"]["deviceName"]
        options.automation_name = self.config["device"]["automationName"]

        # APP CONFIG
        options.app_package = self.config["app"]["appPackage"]
        options.app_activity = self.config["app"]["appActivity"]

        # FLAGS
        options.no_reset = self.config["device"].get("noReset", False)

        # STABILITY
        options.new_command_timeout = 300

        # START DRIVER
        self.driver = webdriver.Remote(
            command_executor=self.config["appium"]["server_url"],
            options=options
        )

        self.driver.implicitly_wait(10)

        print("✅ Driver Started")

        return self.driver

    def stop_driver(self):

        if self.driver:

            print("🛑 Closing Driver")

            self.driver.quit()

            self.driver = None