import pytest
from pages.mobile.login_page import LoginPage
from pages.mobile.side_menu_page import SidebarPage

@pytest.mark.usefixtures("driver")
class TestLogin:

    @pytest.mark.order(1)
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.android
    def test_login(self, driver, config):

        login = LoginPage(driver)
        page = SidebarPage(driver)

        result = login.login(
            config["testdata"]["school"],
            config["testdata"]["phone"]
        )

        assert result, "Login failed"

        login.logout()