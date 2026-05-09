import pytest
from pages.mobile.login_page import LoginPage
from pages.mobile.home_page import HomePage


@pytest.mark.usefixtures("driver")
class TestHome:

    @pytest.mark.order(2)
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.android
    def test_home_full_flow(self, driver, config):

        login = LoginPage(driver)
        home = HomePage(driver)

        print("Full Flow Started")

        # Always fresh login
        login.login(
            config["testdata"]["school"],
            config["testdata"]["phone"]
        )

        assert home.is_logged_in(), "Home not loaded"

        # logout from home
        home.logout()

        # login again
        login.login(
            config["testdata"]["school"],
            config["testdata"]["phone"]
        )
        
        home.verify_all_tabs()

        assert home.is_logged_in()