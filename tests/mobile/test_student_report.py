import pytest
from pages.mobile.student_report_page import StudentReportPage
from pages.mobile.login_page import LoginPage

@pytest.mark.usefixtures("driver")
class TestStudentReport:
    @pytest.mark.order(5)
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.android
    def test_student_report_page(self, driver, config):

        print("🚀 Test Started")

        login = LoginPage(driver)
        page = StudentReportPage(driver)

        login.login(
            config["testdata"]["school"],
            config["testdata"]["phone"]
        )

        page.run_full_student_report_flow()
