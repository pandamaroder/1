import allure
import pytest
from framework.resources.test_params.login_data import BaseLogin
from framework.ui_pages.login_page import LoginPage
from framework.resources.test_params.registration_data import QualityLogin
from framework.ui_pages.RQualityLoginPage import QualityLoginPage

@pytest.mark.positive
@pytest.mark.usefixtures('allure_screen')
@allure.feature('smd.mos.ru Авторизация')
class TestRegistrationForm:

    @pytest.mark.skip('нужны тестовые данные')
    @allure.story('Проверка авторизации')
    @allure.testcase('https://google.com/', name='Ссылка на тест-кейс')
    def test_login(self):
        """
        Описание теста.
        Открыть страницу https://smd.mos.ru/login/
        Заполнить форму авторизации
        Нажать кнопку 'Войти'
        """
        page = LoginPage()
        page.open()
        page.login(BaseLogin.login, BaseLogin.password)


