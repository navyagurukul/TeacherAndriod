from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from appium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from core.base.base_mobile_page import BaseMobilePage
import time


class SidebarPage(BaseMobilePage):

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # SIDE MENU BUTTON
    SIDE_MENU = (
        AppiumBy.XPATH,
        '//android.widget.TextView[@text="󰍜"]'
    )

    # MENU OPTIONS
    DASHBOARD = (
        AppiumBy.XPATH,
        '//android.widget.TextView[@text="Dashboard"]'
    )

    PROFILE = (
        AppiumBy.XPATH,
        '//android.widget.TextView[@text="Profile"]'
    )

    TEST = (
        AppiumBy.XPATH,
        '//android.widget.TextView[@text="Test"]'
    )

    UNLOCK_TOPICS = (
        AppiumBy.XPATH,
        '//android.widget.TextView[@text="Unlock Topics"]'
    )

    LOGOUT = (
        AppiumBy.XPATH,
        '//android.widget.TextView[@text="Logout"]'
    )

    def click(self, locator, name):

        try:
            print(f"Clicking: {name}")

            element = self.wait.until(
                EC.element_to_be_clickable(locator)
            )

            element.click()

            time.sleep(2)

            print(f"Clicked: {name}")

        except Exception as e:
            print(f"Failed to click {name}: {str(e)[:120]}")

    def open_sidebar(self):

        self.click(self.SIDE_MENU, "Side Menu")

    def click_all_sidebar_items(self):

        print("\nStarting sidebar navigation...\n")

        self.open_sidebar()
        self.click(self.DASHBOARD, "Dashboard")

        self.open_sidebar()
        self.click(self.PROFILE, "Profile")

        self.open_sidebar()
        self.click(self.TEST, "Test")

        self.open_sidebar()
        self.click(self.UNLOCK_TOPICS, "Unlock Topics")

        self.open_sidebar()
        self.click(self.LOGOUT, "Logout")

        print("\nSidebar navigation completed")