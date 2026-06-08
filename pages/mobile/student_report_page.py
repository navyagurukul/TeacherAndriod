import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from appium import webdriver
from core.base.base_mobile_page import BaseMobilePage


class StudentReportPage(BaseMobilePage):

    def __init__(self, driver):
        super().__init__(driver)

    # ================= LOCATORS =================

    STUDENT_REPORT_TAB = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='Student Report']"
    )

    # grade dropdown arrow
    GRADE_DROPDOWN = (
        AppiumBy.XPATH,
        '(//android.widget.TextView[@text="󰅀"])[1]'
    )

    # all grades in popup
    GRADE_OPTIONS = (
        AppiumBy.XPATH,
        "//android.view.ViewGroup[contains(@content-desc,'Grade') or contains(@content-desc,'Class') or contains(@content-desc,'UKG') or contains(@content-desc,'LKG') or contains(@content-desc,'ETC') or contains(@content-desc,'CT')]"
    )

    # report toggle
    REPORT_TOGGLE = (
        AppiumBy.CLASS_NAME,
        "android.widget.Switch"
    )

    # ================= ACTIONS =================

    def open_student_report(self):

        self.click(self.STUDENT_REPORT_TAB)

        print("Student Report opened")

        time.sleep(2)

    # ================= GRADES =================

    def get_all_grades(self):

        self.click(self.GRADE_DROPDOWN)

        time.sleep(2)

        elements = self.driver.find_elements(*self.GRADE_OPTIONS)

        grades = []

        for el in elements:

            grade = el.get_attribute("content-desc")

            if grade and grade.strip():

                grades.append(grade.strip())

        grades = list(dict.fromkeys(grades))

        print(f"Grades found: {grades}")

        return grades

    def select_grade(self, grade):

        print(f"Selecting grade: {grade}")
        time.sleep(1)

        locator = (
            AppiumBy.XPATH,
            f'//android.view.ViewGroup[@content-desc="{grade}"]'
        )

        last_err = None
        for attempt in range(3):
            try:
                grade_element = WebDriverWait(self.driver, 8).until(
                    EC.element_to_be_clickable(locator)
                )
                grade_element.click()
                print(f"Selected: {grade}")
                time.sleep(2)
                return
            except Exception as e:
                last_err = e
                # Try scrolling the dropdown to bring the option into view.
                try:
                    self.driver.find_element(
                        AppiumBy.ANDROID_UIAUTOMATOR,
                        f'new UiScrollable(new UiSelector().scrollable(true))'
                        f'.scrollIntoView(new UiSelector().descriptionContains("{grade}"))'
                    )
                except Exception:
                    pass
                time.sleep(1)

        raise last_err

    def select_all_grades(self):

        grades = self.get_all_grades()

        for index, grade in enumerate(grades):

            try:
                self.select_grade(grade)
            except Exception as e:
                print(f"Skipped {grade}: {str(e).splitlines()[0]}")

            # reopen dropdown except last grade
            if index != len(grades) - 1:
                try:
                    self.click(self.GRADE_DROPDOWN)
                    time.sleep(1)
                except Exception as e:
                    print(f"Could not reopen grade dropdown: {str(e).splitlines()[0]}")

        print("All grades selected")

        self.click(self.STUDENT_REPORT_TAB)

        print("Returned back after selecting all grades")

    # ================= TOGGLES =================
    def enable_Assessment_Result(self):

        print("Switching to Assessment Result")

        toggles = self.driver.find_elements(*self.REPORT_TOGGLE)

        if toggles:

            toggle = toggles[0]

            checked = toggle.get_attribute("checked")

            if checked == "false":

                toggle.click()

                print("Switched to Assessment Result")

            else:

                print("Already in Assessment Result")

        time.sleep(2)

    # ================= FULL FLOW =================

    def run_full_student_report_flow(self):
        self.open_student_report()
        self.select_all_grades()
        self.enable_Assessment_Result()
        self.select_all_grades()
        print("Completed Student Report flow")