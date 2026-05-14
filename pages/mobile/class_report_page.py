import time
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from core.base.base_mobile_page import BaseMobilePage


class ClassReportPage(BaseMobilePage):

    def __init__(self, driver):
        super().__init__(driver)

    # ================= LOCATORS =================

    CLASS_REPORT_TAB = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='Class Report']"
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

    # total/monthly toggle
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
    
    SIDE_MENU = (
        AppiumBy.XPATH,
        '//android.widget.TextView[@text="󰍜"]'
    )
    
    LOGOUT = (
        AppiumBy.XPATH,
        '//android.widget.TextView[@text="Logout"]'
    )

    # ================= ACTIONS =================

    def open_class_report(self):

        self.click(self.CLASS_REPORT_TAB)

        print("✅ Class Report opened")

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

        print(f"📚 Grades found: {grades}")

        return grades

    def select_grade(self, grade):

        print(f"➡️ Selecting grade: {grade}")
        time.sleep(1)
        
        grade_element = self.wait.until(
            EC.element_to_be_clickable((
                AppiumBy.XPATH,
                f'//android.view.ViewGroup[@content-desc="{grade}"]'
            ))
        )

        grade_element.click()

        print(f"✅ Selected: {grade}")
        #self.click(self.GRADE_DROPDOWN)

        time.sleep(2)

    def select_all_grades(self):

        grades = self.get_all_grades()

        for index, grade in enumerate(grades):

            self.select_grade(grade)

            # reopen dropdown except last grade
            if index != len(grades) - 1:

                self.click(self.GRADE_DROPDOWN)

                time.sleep(1)

        print("✅ All grades selected")

        self.click(self.CLASS_REPORT_TAB)

        print("↩️ Returned back after selecting all grades")

    # ================= TOGGLES =================

    def toggle_total_monthly(self):

        toggles = self.driver.find_elements(*self.TOTAL_MONTHLY_TOGGLE)

        if len(toggles) > 1:

            toggles[1].click()

            print("✅ Total/Monthly toggled")

        time.sleep(2)

    def enable_test_report(self):

        print("🔄 Switching to Test Report")

        toggles = self.driver.find_elements(*self.REPORT_TOGGLE)

        if toggles:

            toggle = toggles[0]

            checked = toggle.get_attribute("checked")

            if checked == "false":

                toggle.click()

                print("✅ Switched to Test Report")

            else:

                print("✅ Already in Test Report")

        time.sleep(2)

    # ================= ASSESSMENTS =================

    def open_assessment_dropdown(self):
        dropdown = self.wait.until(
            EC.element_to_be_clickable(self.ASSESSMENT_DROPDOWN)
        )
        dropdown.click()

        print("Assessment dropdown opened")
        time.sleep(1)

    def get_assessment_names(self):
        self.open_assessment_dropdown()

        options = self.driver.find_elements(*self.ASSESSMENT_OPTIONS)

        names = [o.text for o in options if o.text.strip()]
        print(f"Assessments: {names}")

        return names

    def select_all_assessments(self):

        selected = set()

        while True:

            # open dropdown
            self.open_assessment_dropdown()

            time.sleep(1)

            # get all visible assessments
            options = self.driver.find_elements(*self.ASSESSMENT_OPTIONS)

            names = [
                o.text.strip()
                for o in options
                if o.text.strip()
            ]

            # remove duplicates
            names = list(dict.fromkeys(names))

            print(f"Current visible options: {names}")

            # find next unselected assessment
            next_item = None

            for name in names:

                if name not in selected:

                    next_item = name
                    break

            # all done
            if not next_item:

                print("✅ All assessments selected")

                # close dropdown / return back
                self.driver.back()

                print("↩️ Returned back after selecting all assessments")

                return

            try:

                print(f"Selecting: {next_item}")

                option = self.wait.until(
                    EC.element_to_be_clickable((
                        AppiumBy.XPATH,
                        f'//android.widget.TextView[@text="{next_item}"]'
                    ))
                )

                option.click()

                selected.add(next_item)

                print(f"Selected so far: {selected}")

                time.sleep(1)

            except Exception as e:

                print(f"❌ Error selecting {next_item}: {e}")

                return

    def select_assessment_for_each_grade(self):

        # open grade dropdown once
        grades = self.get_all_grades()

        for index, grade in enumerate(grades):

            print(f"\n📘 Processing Grade: {grade}")

            try:

                # select grade
                self.select_grade(grade)

                # wait for assessment dropdown
                self.wait.until(
                    EC.presence_of_element_located(
                        self.ASSESSMENT_DROPDOWN
                    )
                )

                self.wait.until(
                    EC.element_to_be_clickable(
                        self.ASSESSMENT_DROPDOWN
                    )
                )

                time.sleep(2)

                # select all assessments
                self.select_all_assessments()

                print(f"✅ Completed assessments for {grade}")

                # reopen dropdown except for last grade
                if index != len(grades) - 1:

                    self.click(self.GRADE_DROPDOWN)

                    time.sleep(1)

                else:

                    print("✅ All grades completed")

            except Exception as e:

                print(f"❌ Assessment issue for {grade}: {e}")

    def open_sidebar(self):

        self.click(self.SIDE_MENU, "Side Menu")
    # ================= FULL FLOW =================

    def run_full_class_report_flow(self):
        self.open_class_report()
        self.select_all_grades()
        self.toggle_total_monthly()
        self.enable_test_report()
        #self.select_all_grades()
        self.select_assessment_for_each_grade()
        self.open_sidebar()
        self.click(self.LOGOUT, "Logout")

        print("Completed Class Report flow")