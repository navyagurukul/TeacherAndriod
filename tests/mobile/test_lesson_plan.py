import pytest
from pages.mobile.lesson_plan_page import LessonPlanPage
from pages.mobile.login_page import LoginPage
from pages.mobile.home_page import HomePage


@pytest.mark.usefixtures("driver")
class TestLessonPlan:
    @pytest.mark.order(3)
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.android
    def test_lesson_plan_pdfs(self, driver, config):

        print("Test Started")

        login = LoginPage(driver)
        home = HomePage(driver)
        page = LessonPlanPage(driver)

        login.login(
            config["testdata"]["school"],
            config["testdata"]["phone"]
        )

        assert home.is_logged_in(), "❌ Login failed"

        page.run_grade_selection_flow()
