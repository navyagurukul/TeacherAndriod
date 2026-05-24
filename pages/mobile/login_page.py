from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from appium import webdriver
from core.base.base_mobile_page import BaseMobilePage
import time


class LoginPage(BaseMobilePage):
    def __init__(self, driver):
        super().__init__(driver)

    # ===== LOCATORS =====

    SEARCH_SCHOOL = (AppiumBy.XPATH, "//android.widget.TextView[@text='Search your school']")
    SCHOOL_INPUT = (AppiumBy.XPATH, "//android.widget.EditText[@text='Type here...']")
    SCHOOL_OPTION = (AppiumBy.XPATH, "//android.widget.TextView[contains(@text,'Sanskruthi School')]")
    PHONE_INPUT = (AppiumBy.XPATH, "//android.widget.EditText[contains(@text,'mobile')]")
    LOGIN_BTN = (AppiumBy.XPATH, "//android.widget.TextView[@text='Login']")
    HOME_TEXT = (AppiumBy.XPATH, "//android.widget.TextView[contains(@text,'Home')]")

    #  BEST MENU LOCATOR (NO Unicode, NO WhatsApp issue)
    MENU_BTN = (AppiumBy.XPATH, "//android.widget.ImageButton[@clickable='true']")

    LOGOUT_BTN = (AppiumBy.XPATH, "//android.widget.TextView[@text='Logout']")

    # ===== ACTIONS =====

    def login(self, school, phone):
        print("Login Flow Started")

        self.wait.until(EC.presence_of_element_located(self.SEARCH_SCHOOL))

        self.click(self.SEARCH_SCHOOL)
        self.send_keys(self.SCHOOL_INPUT, school)

        self.wait.until(EC.element_to_be_clickable(self.SCHOOL_OPTION))
        self.click(self.SCHOOL_OPTION)

        self.send_keys(self.PHONE_INPUT, phone)
        self.click(self.LOGIN_BTN)

        self.wait.until(EC.presence_of_element_located(self.HOME_TEXT))

        print("Login Successful")
        return True

    # ===== MENU =====

    def open_menu(self):
        print("Opening Menu")

        time.sleep(0.5)

        try:
            menu = self.wait.until(
                EC.element_to_be_clickable(self.MENU_BTN)
            )
            menu.click()
            print("Menu clicked")
        except Exception as e:
            print("Fallback tap used:", e)

            size = self.driver.get_window_size()
            x = int(size['width'] * 0.92)
            y = int(size['height'] * 0.08)

            self.driver.tap([(x, y)])

    # ===== LOGOUT =====

    def logout(self):
        print("Logout Flow")

        self.open_menu()

        self.wait.until(
            EC.element_to_be_clickable(self.LOGOUT_BTN)
        ).click()

        print("Logout done")