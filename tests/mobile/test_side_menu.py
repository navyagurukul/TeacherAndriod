import pytest
from pages.mobile.side_menu_page import SidebarPage
from pages.mobile.login_page import LoginPage


@pytest.mark.usefixtures("driver")
class TestSideMenu:
    @pytest.mark.order(7)
    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.android
    def test_side_menu_page(self, driver, config):

        print("Test Started")

        login = LoginPage(driver)
        page = SidebarPage(driver)

        # LOGIN
        login.login(
            config["testdata"]["school"],
            config["testdata"]["phone"]
        )
        
        page.click_all_sidebar_items()