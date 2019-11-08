from selene.browser import open_url
from selene.support.jquery_style_selectors import s


class LoginPage(object):
    def __init__(self):
        self.loginField = s('[name="login"]')
        self.passwordField = s('[name="password"]')
        self.loginButton = s('button')

    def open(self):
        open_url('login/')
        return self

    def login(self, login, password):
        self.loginField.set(login)
        self.passwordField.set(password)
        print("ftftyfgh")
        self.loginButton.click()
        # return AfterLoginPage()
