import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from core.base.base_mobile_page import BaseMobilePage


class ClassReportPage(BaseMobilePage):

    def __init__(self, driver):
        super().__init__(driver)

    # ================= LOCATORS =================

    CLASS_REPORT_TAB = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='Class Report']"
    )

    GRADE_DROPDOWN = (
        AppiumBy.XPATH,
        '(//android.widget.TextView[@text="󰅀"])[1]'
    )

    GRADE_OPTIONS = (
        AppiumBy.XPATH,
        "//android.view.ViewGroup[contains(@content-desc,'Grade') or contains(@content-desc,'Class')]"
    )

    REPORT_TOGGLE = (
        AppiumBy.CLASS_NAME,
        "android.widget.Switch"
    )

    TOTAL_MONTHLY_TOGGLE = (
        AppiumBy.CLASS_NAME,
        "android.widget.Switch"
    )

    ASSESSMENT_DROPDOWN = (
        AppiumBy.XPATH,
        "//android.view.ViewGroup[contains(@content-desc,'Assessment') or contains(@content-desc,'Assesment')]"
    )

    ASSESSMENT_OPTIONS = (
        AppiumBy.XPATH,
        "//android.widget.TextView[contains(@text,'Assessment') or contains(@text,'Assesment')]"
    )

    # ================= HELPERS =================

    def wait_clickable(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_present(self, locator, timeout=15):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    # ================= CLASS REPORT =================

    def open_class_report(self):
        self.wait_clickable(self.CLASS_REPORT_TAB).click()
        print("Class Report opened")

    # ================= GRADES =================

    def get_all_grades(self):

        self.wait_clickable(self.GRADE_DROPDOWN).click()
        time.sleep(2)

        elements = self.driver.find_elements(*self.GRADE_OPTIONS)

        grades = []
        for el in elements:
            val = el.get_attribute("content-desc")
            if val and val.strip():
                grades.append(val.strip())

        grades = list(dict.fromkeys(grades))
        print(f"Grades found: {grades}")

        return grades

    def select_grade(self, grade):

        print(f"Selecting grade: {grade}")

        locator = (
            AppiumBy.XPATH,
            f'//android.view.ViewGroup[@content-desc="{grade}"]'
        )

        self.wait_clickable(locator).click()

        print(f"Selected: {grade}")
        time.sleep(2)

    def select_all_grades(self):

        grades = self.get_all_grades()

        for i, grade in enumerate(grades):

            self.select_grade(grade)

            if i != len(grades) - 1:
                self.wait_clickable(self.GRADE_DROPDOWN).click()
                time.sleep(1)

        print("All grades selected")

        self.wait_clickable(self.CLASS_REPORT_TAB).click()
        print("Returned back after selecting all grades")

    # ================= TOGGLES =================

    def toggle_total_monthly(self):

        toggles = self.driver.find_elements(*self.TOTAL_MONTHLY_TOGGLE)

        if len(toggles) > 1:
            toggles[1].click()
            print("Total/Monthly toggled")

        time.sleep(2)

    def enable_test_report(self):

        toggles = self.driver.find_elements(*self.REPORT_TOGGLE)

        if toggles:
            toggle = toggles[0]

            if toggle.get_attribute("checked") == "false":
                toggle.click()
                print("Switched to Test Report")

        time.sleep(2)

    # ================= ASSESSMENTS (FIXED) =================

    def open_assessment_dropdown(self):

        self.wait_present(self.ASSESSMENT_DROPDOWN)
        self.wait_clickable(self.ASSESSMENT_DROPDOWN).click()

        print("Assessment dropdown opened")
        time.sleep(2)

    def select_all_assessments(self):

        selected = set()

        for _ in range(20):

            try:
                self.open_assessment_dropdown()

                options = self.driver.find_elements(*self.ASSESSMENT_OPTIONS)

                names = [
                    o.text.strip()
                    for o in options
                    if o.text and o.text.strip()
                ]

                found_new = False

                for name in names:

                    if name in selected:
                        continue

                    print(f"Selecting: {name}")

                    locator = (
                        AppiumBy.XPATH,
                        f"//android.widget.TextView[@text='{name}']"
                    )

                    self.wait_clickable(locator).click()

                    selected.add(name)

                    print(f"Selected: {selected}")

                    time.sleep(2)

                    found_new = True
                    break

                if not found_new:
                    print("All assessments processed")
                    return

            except Exception as e:
                print(f"Retrying due to: {e}")
                time.sleep(2)

    def get_assessment_state(self):

        source = self.driver.page_source.lower()

        if "locked" in source:
            return "locked"
        if "resume" in source or "continue" in source:
            return "in_progress"
        if "completed" in source:
            return "completed"
        if "closed" in source:
            return "closed"

        return "open"

    # ================= FULL FLOW =================

    def select_assessment_for_each_grade(self):

        grades = self.get_all_grades()

        for i, grade in enumerate(grades):

            print(f"\nProcessing Grade: {grade}")

            try:
                self.select_grade(grade)

                self.wait_present(self.ASSESSMENT_DROPDOWN)
                self.wait_clickable(self.ASSESSMENT_DROPDOWN)

                self.select_all_assessments()

                print(f"Completed assessments for {grade}")

                if i != len(grades) - 1:
                    self.wait_clickable(self.GRADE_DROPDOWN).click()
                    time.sleep(1)
                else:
                    print("All grades completed")

            except Exception as e:
                print(f"Assessment issue for {grade}: {e}")

    # ================= MAIN FLOW =================

    def run_full_class_report_flow(self):

        self.open_class_report()
        self.select_all_grades()
        self.toggle_total_monthly()
        self.enable_test_report()
        self.select_assessment_for_each_grade()

        print("Completed Class Report flow")