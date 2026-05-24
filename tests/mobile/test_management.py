import pytest
from pages.mobile.management_page import StudentManagementPage
from pages.mobile.login_page import LoginPage


@pytest.mark.usefixtures("driver")
class TestManagement:
    @pytest.mark.order(6)
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.android
    def test_management_page(self, driver, config):

        print("🚀 Test Started")

        login = LoginPage(driver)
        management = StudentManagementPage(driver)

        # LOGIN
        login.login(
            config["testdata"]["school"],
            config["testdata"]["phone"]
        )

        # OPEN MANAGEMENT
        management.open_management()

        # REGISTER STUDENT PAGE
        management.register_student()

        # STUDENT APPROVAL PAGE
        management.open_student_approval()

        # EDIT STUDENT PAGE
        management.edit_student()

        # DELETE STUDENT PAGE
        management.delete_student()

        print("Student Management flow completed successfully")