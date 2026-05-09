import pytest
from pages.mobile.login_page import LoginPage


@pytest.mark.usefixtures("driver")
class TestLogin:

    @pytest.mark.order(1)
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.android
    def test_login(self, driver, config):

        login = LoginPage(driver)

        result = login.login(
            config["testdata"]["school"],
            config["testdata"]["phone"]
        )

        assert result, "Login failed"

        login.logout()