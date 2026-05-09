import pytest
from core.driver.appium_driver import AppiumDriver
from utils.config_reader import load_config


class BaseMobileTest:

    @pytest.fixture(scope="function", autouse=True)
    def setup(self, request):

        config = load_config()

        app_driver = AppiumDriver(config)

        driver = app_driver.start_driver()

        request.cls.driver = driver
        request.cls.config = config

        yield

        app_driver.stop_driver()