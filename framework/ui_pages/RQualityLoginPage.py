import os

import allure
from selene.browser import open_url
from selene.conditions import visible, enabled, text
from selene.support import by
from selene.support.conditions import have
from selene.support.jquery_style_selectors import s, ss
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys

class QualityLoginPage(object):
    def __init__(self):
        self.loginField = s('[name="Username"]')
        self.passwordField = s('[name="Password"]')
        self.loginButton = s('[name="button"]')

        @allure.step("Открыть страницу аутентификации qualitycentral.dev.local")
        def open(self):
            # костыль, отключает пераметр base_url из defaults.ini, используем абсолютный url: https://timepad.ru
            from selene import config
            config.base_url = ""

            open_url('http://192.168.10.151/auth/identity/account/login')
            return self

        @allure.step("Нажать кнопку 'Войти' и заполнить форму авторизации")
        def login(self, login, password):
            self.loginField.set(login)
            self.passwordField.set(password)
            self.loginButton.click()