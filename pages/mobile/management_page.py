from appium.webdriver.common.appiumby import AppiumBy
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.base.base_mobile_page import BaseMobilePage
import time


class StudentManagementPage(BaseMobilePage):
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    # ================= LOCATORS =================

    MANAGEMENT_TAB = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='Management']"
    )

    MANAGEMENT_HEADER = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='Student Management']"
    )

    REGISTER_CARD = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='Student Registration']"
    )

    APPROVAL_CARD = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='Student Approval']"
    )

    EDIT_CARD = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='Edit Student']"
    )

    DELETE_CARD = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='Delete Student']"
    )

    STUDENT_NAME_INPUT = (
        AppiumBy.XPATH,
        "//android.widget.EditText[contains(@text,'Student Name')]"
    )

    FATHER_NAME_INPUT = (
        AppiumBy.XPATH,
        "//android.widget.EditText[contains(@text,\"Father's Name\")]"
    )

    MOBILE_INPUT = (
        AppiumBy.XPATH,
        "//android.widget.EditText[contains(@text,'Mobile Number')]"
    )

    GENDER_DROPDOWN = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='Gender']/following-sibling::*"
    )

    LANGUAGE_DROPDOWN = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='Language']/following-sibling::*"
    )

    GRADE_DROPDOWN = (
        AppiumBy.XPATH,
        '//android.view.ViewGroup[@content-desc="Grade"]/android.widget.ImageView'
    )

    GRADE_OPTIONS = (
        AppiumBy.XPATH,
        "//android.widget.TextView[contains(@text,'Grade')]"
    )

    SUBMIT_REVIEW_BTN = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='Submit & Review']"
    )

    CONFIRM_BUTTON = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='Confirm']"
    )

    REGISTER_ALL_BTN = (
        AppiumBy.XPATH,
        "//android.widget.TextView[@text='Register All Students']"
    )

    BACK_BTN = (
        AppiumBy.XPATH,
        "//android.view.ViewGroup[@content-desc='󰁍']"
    )

    # ================= COMMON METHODS =================

    def wait_for_management_screen(self):
        self.wait.until(
            EC.visibility_of_element_located(self.MANAGEMENT_HEADER)
        )

    def open_management(self):
        print("Opening Management tab...")

        self.click(self.MANAGEMENT_TAB)

        self.wait_for_management_screen()

        print("Management screen loaded")

    def click(self, locator):
        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def send_keys(self, locator, text):
        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )
        return element.text

    def safe_click(self, locator):

        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )

        element.click()

    def open_card(self, locator, name):

        print(f"Opening {name}...")

        card = self.wait.until(
            EC.element_to_be_clickable(locator)
        )

        card.click()

        print(f"{name} opened")

    def go_back(self):

        print("Going back...")

        try:

            back_btn = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.BACK_BTN)
            )

            back_btn.click()

            print("Back button clicked")

        except Exception:

            print("Toolbar back not found → using device back")

            self.driver.back()

    def safe_back_to_management(self):

        print("Navigating back to Management...")

        try:

            self.go_back()

            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(
                    self.MANAGEMENT_HEADER
                )
            )

            print("Back to Management")

        except Exception:

            print("Still not on Management screen")

            # TRY DEVICE BACK AGAIN
            self.driver.back()

            time.sleep(2)

            try:

                self.wait.until(
                    EC.visibility_of_element_located(
                        self.MANAGEMENT_HEADER
                    )
                )

                print("Returned to Management")

            except Exception:

                print("Opening Management manually")

                self.open_management()

    # ================= DROPDOWNS =================

    def select_dropdown_option(self, dropdown_locator, option_text):

        print(f"Selecting {option_text}")

        dropdown = self.wait.until(
            EC.element_to_be_clickable(dropdown_locator)
        )

        dropdown.click()

        option = self.wait.until(
            EC.element_to_be_clickable((
                AppiumBy.XPATH,
                f"//android.widget.TextView[@text='{option_text}']"
            ))
        )

        option.click()

    def select_any_grade(self):

        print("Selecting available grade...")

        # OPEN DROPDOWN
        self.click(self.GRADE_DROPDOWN)

        time.sleep(1)

        # GET ALL GRADE OPTIONS
        options = self.wait.until(
            EC.presence_of_all_elements_located((
                AppiumBy.XPATH,
                "//android.widget.TextView[contains(@text,'Grade')]"
            ))
        )

        if not options:
            raise Exception("No grade options found")

        # SELECT FIRST AVAILABLE GRADE
        option = options[3]

        print(f"Selected: {option.text}")

        option.click()

        time.sleep(1)

        print("Grade selected successfully")

    # ================= BUTTON ACTIONS =================
    def scroll_down(self):

        self.driver.execute_script(
            "mobile: scrollGesture",
            {
                "left": 100,
                "top": 300,
                "width": 800,
                "height": 1400,
                "direction": "down",
                "percent": 0.8
            }
        )

        time.sleep(1)

    def click_submit_review(self):

        print("Scrolling to Submit & Review...")

        for _ in range(5):

            try:
                btn = self.wait.until(
                    EC.presence_of_element_located(self.SUBMIT_REVIEW_BTN)
                )

                # bring button into view
                self.driver.execute_script(
                    "mobile: scrollGesture",
                    {
                        "left": 100,
                        "top": 300,
                        "width": 800,
                        "height": 1400,
                        "direction": "down",
                        "percent": 0.7
                    }
                )

                time.sleep(1)

                try:
                    btn.click()

                except Exception:
                    # fallback tap
                    loc = btn.location
                    size = btn.size

                    x = loc['x'] + size['width'] // 2
                    y = loc['y'] + size['height'] // 2

                    self.driver.tap([(x, y)])

                print("✅ Submit & Review clicked")

                return

            except Exception:

                self.scroll_down()

        raise Exception("❌ Submit & Review button not found")

    def click_confirm(self):

        print("Clicking Confirm")

        confirm = self.wait.until(
            EC.element_to_be_clickable(self.CONFIRM_BUTTON)
        )

        confirm.click()

    def click_register_all_students(self):

        print("Clicking Register All Students")

        btn = self.wait.until(
            EC.element_to_be_clickable(self.REGISTER_ALL_BTN)
        )

        btn.click()

    # ================= MAIN FLOWS =================

    def register_student(self):

        self.open_card(self.REGISTER_CARD, "Student Registration")

        print("Student Registration page opened")

        self.send_keys(self.STUDENT_NAME_INPUT, "QA Student")
        self.send_keys(self.FATHER_NAME_INPUT, "Testing")
        self.send_keys(self.MOBILE_INPUT, "9876543213")

        self.select_dropdown_option(
            self.GENDER_DROPDOWN,
            "Female"
        )

        time.sleep(1)

        self.select_any_grade()

        time.sleep(1)

        self.select_dropdown_option(
            self.LANGUAGE_DROPDOWN,
            "English"
        )

        self.click_submit_review()

        time.sleep(1)

        self.click_confirm()

        time.sleep(1)

        self.click_register_all_students()

        print("Student registered successfully")

        time.sleep(2)

        self.safe_back_to_management()

    def open_student_approval(self):

        self.open_card(self.APPROVAL_CARD, "Student Approval")

        time.sleep(1)

        self.safe_back_to_management()

    def edit_student(self):

        self.open_card(self.EDIT_CARD, "Edit Student")

        time.sleep(1)

        self.safe_back_to_management()

    def delete_student(self):

        self.open_card(self.DELETE_CARD, "Delete Student")
        self.safe_back_to_management()
        self.click(self.MANAGEMENT_TAB)