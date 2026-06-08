import time
from appium.webdriver.common.appiumby import AppiumBy
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.base.base_mobile_page import BaseMobilePage


class LessonPlanPage(BaseMobilePage):

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    # ================= LOCATORS =================

    LESSON_PLAN_TAB = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='Lesson Plan']"
    )

    GRADE_DROPDOWN = (
        AppiumBy.XPATH,
        "//*[contains(@text,'Grade') or contains(@text,'Class') or contains(@text,'ETC') or contains(@text,'CT') or contains(@text,'UKG') or contains(@text,'LKG')]"
    )

    GRADE_OPTIONS = (
        AppiumBy.CLASS_NAME,
        "android.widget.TextView"
    )

    # ================= ACTIONS =================

    def open_lesson_plan(self):
        self.wait.until(
            EC.element_to_be_clickable(self.LESSON_PLAN_TAB)
        ).click()
        print("Lesson Plan opened")

    def get_grades(self):
        # open dropdown
        self.wait.until(
            EC.element_to_be_clickable(self.GRADE_DROPDOWN)
        ).click()
        time.sleep(1)

        elements = self.driver.find_elements(*self.GRADE_OPTIONS)

        grades = []
        for el in elements:
            text = el.text.strip()

            if text and text.lower().startswith("grade"):
                grades.append(text)

        print("Grades found:", grades)
        return grades

    def select_grade(self, grade):
        print(f"Selecting grade: {grade}")

        option_locator = (AppiumBy.XPATH, f"//*[@text='{grade}']")

        last_err = None
        for attempt in range(3):
            try:
                triggers = self.driver.find_elements(*self.GRADE_DROPDOWN)
                if triggers:
                    # Take the LAST match — the dropdown trigger sits below
                    # any previously selected grade text shown in the page.
                    triggers[-1].click()
                time.sleep(1)

                option = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable(option_locator)
                )
                option.click()

                print(f"Selected: {grade}")
                time.sleep(2)
                return
            except Exception as e:
                last_err = e
                time.sleep(1)

        raise last_err

    # ================= FLOW =================

    def run_grade_selection_flow(self):
        self.open_lesson_plan()

        grades = self.get_grades()

        for grade in grades:
            try:
                self.select_grade(grade)
            except Exception as e:
                print(f"Failed selecting {grade}: {str(e)[:80]}")