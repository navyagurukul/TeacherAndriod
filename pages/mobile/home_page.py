from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from appium import webdriver
from core.base.base_mobile_page import BaseMobilePage
import time


class HomePage(BaseMobilePage):
    def __init__(self, driver):
        super().__init__(driver)

    HOME_TEXT = (AppiumBy.XPATH, "//android.widget.TextView[contains(@text,'Home')]")
    LESSON_PLAN_TAB = (AppiumBy.XPATH, "//android.widget.TextView[@text='Lesson Plan']")
    CLASS_REPORT_TAB = (AppiumBy.XPATH, "//android.widget.TextView[@text='Class Report']")
    STUDENT_REPORT_TAB = (AppiumBy.XPATH, "//android.widget.TextView[@text='Student Report']")
    MANAGEMENT_TAB = (AppiumBy.XPATH, "//android.widget.TextView[@text='Management']")
    LOGOUT_BTN = (AppiumBy.XPATH, "//android.widget.TextView[@text='Logout']")

    MENU_BTN = (
        AppiumBy.XPATH,
        "//android.widget.ImageButton[@clickable='true']"
        " | //android.widget.ImageView[@clickable='true' and contains(@content-desc,'enu')]"
        " | //*[@content-desc='Menu' or @content-desc='menu' or @content-desc='Open menu']"
    )

    def is_logged_in(self):
        return self.is_visible(self.HOME_TEXT)
    print("Home Page Loaded")
    
    def verify_all_tabs(self):
        print("Verifying all tabs")

        self.wait.until(EC.presence_of_element_located(self.LESSON_PLAN_TAB)).click()
        self.wait.until(EC.presence_of_element_located(self.CLASS_REPORT_TAB)).click()
        self.wait.until(EC.presence_of_element_located(self.STUDENT_REPORT_TAB)).click()
        self.wait.until(EC.presence_of_element_located(self.MANAGEMENT_TAB)).click()

        print("All Tabs Verified")

    def open_menu(self):
        print("Opening Menu")

        time.sleep(1)

        try:
            menu = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable(self.MENU_BTN)
            )
            menu.click()
            print("Menu clicked")
        except Exception:
            size = self.driver.get_window_size()
            x = int(size['width'] * 0.92)
            y = int(size['height'] * 0.08)

            self.driver.tap([(x, y)])
            print("Menu tapped via coordinates")

    def logout(self):
        print("Home Logout")
        
        self.open_menu()

        self.wait.until(
            EC.element_to_be_clickable(self.LOGOUT_BTN)
        ).click()