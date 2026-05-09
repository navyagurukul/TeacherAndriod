import pytest
from pages.mobile.class_report_page import ClassReportPage
from pages.mobile.login_page import LoginPage

@pytest.mark.usefixtures("driver")
class TestClassReport:
    @pytest.mark.order(4)
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.android
    def test_class_report_page(self, driver, config):

        print("🚀 Test Started")

        login = LoginPage(driver)
        page = ClassReportPage(driver)

        login.login(
            config["testdata"]["school"],
            config["testdata"]["phone"]
        )

        page.run_full_class_report_flow()
