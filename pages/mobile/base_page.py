from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class BasePage:

    def __init__(self, driver):

        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def click(self, locator):

        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )

        element.click()

    def find(self, locator):

        return self.wait.until(
            EC.presence_of_element_located(locator)
        )

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

    def is_displayed(self, locator):

        try:
            element = self.wait.until(
                EC.visibility_of_element_located(locator)
            )

            return element.is_displayed()

        except:
            return False

    def scroll_down(self):

        size = self.driver.get_window_size()

        start_x = size["width"] // 2
        start_y = int(size["height"] * 0.80)

        end_x = size["width"] // 2
        end_y = int(size["height"] * 0.30)

        self.driver.swipe(
            start_x,
            start_y,
            end_x,
            end_y,
            800
        )