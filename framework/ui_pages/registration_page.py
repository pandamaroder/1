import os

import allure
from selene.browser import open_url
from selene.conditions import visible, enabled, text
from selene.support import by
from selene.support.conditions import have
from selene.support.jquery_style_selectors import s, ss
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
import psycopg2




class RegistrationPage(object):
    def __init__(self):
        self.title = s('.sub-header')
        self.organizationField = s(by.xpath("//*[text()='Наименование организации']"
                                            "/ancestor::div[contains(@class, 'ErrorNotificator')]"))
        self.userNameField = s(by.xpath("//*[text()='Ф.И.О. пользователя полностью']"
                                        "/ancestor::div[contains(@class, 'ErrorNotificator')]"))
        self.emailField = s(by.xpath("//*[text()='Рабочая электронная почта']"
                                     "/ancestor::div[contains(@class, 'ErrorNotificator')]"))
        self.phoneField = s(by.xpath("//*[text()='Номер телефона для связи с пользователем']"
                                     "/ancestor::div[contains(@class, 'ErrorNotificator')]"))
        self.mobileOsField = s(by.xpath("//*[text()='Операционная система мобильного устройства']"
                                        "/ancestor::div[contains(@class, 'ErrorNotificator')]"))
        self.googlePlayField = s(by.xpath("//*[text()='Учётная запись в Google Play']"
                                          "/ancestor::div[contains(@class, 'ErrorNotificator')]"))
        self.loginCheckBox = s(by.xpath("//input[@type='checkbox']"))
        self.loginField = s(by.xpath("//*[text()='Логин пользователя']"
                                     "/ancestor::div[contains(@class, 'ErrorNotificator')]"))
        self.scanUpload = s(by.xpath("//input[@type='file' and @class='upload-input']"))
        self.loginButton = s(by.xpath("//*[text()='Отправить']/ancestor::button"))
        self.formErrors = ss('.error')

    @allure.step('Открыть страницу регистрации')
    def open(self):
        open_url('registration/')
        self.title.should(visible)
        return self

    @allure.step('Проверка наличия ошибок на странице')
    def assert_page_errors(self):
        error_list = []
        for error in self.formErrors:
            error_list.append(error.text)
        if len(error_list) > 0:
            assert False, "Ошибки на странице:\n" + "\n".join(error_list)

    def populate_field(self, field, value, assert_on_fail=True):
        field_info = field.text
        field_input = field.s('input')
        field_input.scroll_to()
        field_input.set_value(value)
        field_errors = field.ss('.error')
        if field_input.get_attribute('value') == value and len(field_errors) == 0:
            return True
        elif assert_on_fail:
            assert False, f'Ошибки при заполнении поля: {field_info}. Данные: {value}'
        return False

    def auto_create_login_check(self):
        checkbox = self.loginCheckBox.get_actual_webelement()
        if not checkbox.is_selected():
            checkbox.send_keys(Keys.SPACE)
        self.loginField.s('input').should_not(enabled)

    def auto_create_login_uncheck(self):
        checkbox = self.loginCheckBox.get_actual_webelement()
        if checkbox.is_selected():
            checkbox.send_keys(Keys.SPACE)
        self.loginField.s('input').should(enabled)

    @allure.step('Выбор организации из списка по названию: {value}')
    def select_organization(self, value):
        organization_input = self.organizationField.s('input')
        organization_errors = self.organizationField.ss('.error')
        organization_input.click()
        organization_list = s(by.xpath("//*[@role='menu']"))
        organization_list.should(visible)
        try:
            value_to_select = organization_list.s(by.xpath(f"//*[text()='{value}']/ancestor::*[@role='menuitem']"))
            value_to_select.click()
            organization_list.should_not(visible)
        except (TimeoutException, NoSuchElementException):
            return False
        return organization_input.get_attribute('value') == value and len(organization_errors) == 0

    @allure.step('Ручной ввод названия организации, отсутствующей в списке: {value}')
    def populate_none_exist_organization(self, value):
        self.populate_field(self.organizationField, value, False)
        self.title.click()
        self.organizationField.s('input').should(have.value(''))

    @allure.step('Заполнение поля ФИО: {value}')
    def populate_user_name(self, value, assert_on_fail=True):
        return self.populate_field(self.userNameField, value, assert_on_fail)

    @allure.step('Заполнение поля Электронная почта: {value}')
    def populate_email(self, value, assert_on_fail=True):
        return self.populate_field(self.emailField, value, assert_on_fail)

    @allure.step('Заполнение поля Телефон: {value}')
    def populate_phone(self, value, assert_on_fail=True):
        return self.populate_field(self.phoneField, value, assert_on_fail)

    @allure.step('Выбор мобильной ОС: {value}')
    def select_mobile_os(self, value):
        self.mobileOsField.s('button').click()
        mobile_os_list = s(by.xpath("//*[@role='menu']"))
        mobile_os_list.should(visible)
        value_to_select = mobile_os_list.s(by.xpath(f"//*[text()='{value}']/ancestor::*[@role='menuitem']"))
        value_to_select.click()
        mobile_os_list.should_not(visible)
        assert value in self.mobileOsField.text, f'Мобильная ОС: {value} не выбрана'

    def google_play_field_disabled_check(self):
        self.googlePlayField.s('input').should_not(enabled)

    @allure.step('Заполнение поля Google Play: {value}')
    def populate_google_play(self, value, assert_on_fail=True):
        self.googlePlayField.s('input').should(enabled)
        return self.populate_field(self.googlePlayField, value, assert_on_fail)

    @allure.step('Заполнение поля Логин пользователя: {value}')
    def populate_login(self, value, assert_on_fail=True):
        self.auto_create_login_uncheck()
        self.loginField.s('input').should(enabled)
        return self.populate_field(self.loginField, value, assert_on_fail)

    @allure.step('Загрузка скана: {img_path}')
    def upload_scan_image(self, img_path, assert_on_fail=True):
        img_path = os.path.abspath(img_path)
        self.scanUpload.get_actual_webelement().send_keys(img_path)
        img_name = os.path.basename(img_path)
        result_text = s('.input-info').text
        if img_name in result_text or 'Выбрано:' in result_text:
            return True
        elif assert_on_fail:
            assert False, f'Не удалось приложить файл: {img_path}'
        return False

### AFTERREGISTRATION_FIELD_PENS_PROJECT_TESTING

class AfterRegistrationPage(object):
    def __init__(self):
        self.organization2Field = s(by.xpath("//*[text()='Поиск']"
                                             "/ancestor::div[contains(@class, 'ErrorNotificator')]"))
        self.loginField = s('[name="login"]')
        self.passwordField = s('[name="password"]')
        self.loginButton = s('button')

    def open(self):
        open_url('login/')
        return self

    def login(self, login, password):
        self.loginField.set(login)
        self.passwordField.set(password)
        self.loginButton.click()

    def populate_field(self, field, value, assert_on_fail=True):
        field_info = field.text
        field_input = field.s('input')
        field_input.scroll_to()
        field_input.set_value(value)
        field_errors = field.ss('.error')
        if field_input.get_attribute('value') == value and len(field_errors) == 0:
            return True
        elif assert_on_fail:
            assert False, f'Ошибки при заполнении поля: {field_info}. Данные: {value}'
        return False

    @allure.step('Заполнение поля Наименование организации: {value}')
    def organization2_populate(self, value, assert_on_fail=True):
        return self.populate_field(self.organization2Field, value, assert_on_fail)


    def open2(self):
        open_url('administration/')
        return self

class TimepadPage(object):
    def __init__(self):
        self.sign_link = s(by.xpath("//a[text()='Войти']"))
        self.email_field = s('[name="mail"]')
        self.password_field = s('[name="password"]')
        self.login_button = s('#login_form_submit')
        self.user_settings_link = s('#js-usermenu-dropdown')
        self.cookie_accept_button = s('a.js-cookie-consent-accept')
        self.create_new_event_button = s('#publishEvent1')


    @allure.step("Открыть страницу https://timepad.ru")
    def open(self):
        # костыль, отключает пераметр base_url из defaults.ini, используем абсолютный url: https://timepad.ru
        from selene import config
        config.base_url = ""

        open_url('https://timepad.ru/')
        return self

    @allure.step("Нажать кнопку 'Войти' и заполнить форму авторизации")
    def login(self, email, password):
        self.cookie_accept_button.click()
        self.accept_cookie_if_exist()
        self.sign_link.click()
        self.email_field.set(email)
        self.password_field.set(password)
        self.login_button.click()

# in case of accept_cookie_if_exist there is no necessity to initialize in self , becouse it is not relevant functionality

    @allure.step("Проверить что авторизовались успешно (появилась ссылка на личный кабинет)")
    def check_auth(self, user_name):
        self.user_settings_link.should(visible)
        self.user_settings_link.should_have(text(user_name))

    @allure.step("Нажать кнопку 'Хорошо' в окне согласие на обработку cookie и персональных данных")
    def accept_cookie_if_exist(self):
        if self.cookie_accept_button.is_displayed():
            self.cookie_accept_button.click()

    @allure.step("Нажать кнопку 'Опубликовать событие'")
    def create_event_button_click(self):
        self.create_new_event_button.click()
        return TimepadNewEventPage()



class TimepadNewEventPage(object):
    def __init__(self):
        self.event_title = s('#title')
        self.event_description = s('#shortdescription')
        self.event_date_start = s('#datestart')
        self.event_time_start = s('#timestart')
        self.event_date_end = s('#dateend')
        self.event_time_end = s('#timeend')
        self.event_city = s('#token-input-city')
        self.event_category = s('[name="category[]"]')
        self.event_submit_button = s('#submit_send')
        self.addition_settings_link = s(by.xpath("//a[text()='Дополнительные настройки']"))
        self.event_settings_block = s('#event-settings')
        self.add_partner_link = s('#add-partner')

    @allure.step("Заполнить поле 'Название'")
    def set_title(self, title):
        self.populate_field(self.event_title, "Имя события", title)

    @allure.step("Заполнить поле 'Краткое описание'")
    def set_description(self, description):
        self.populate_field(self.event_description, "Описание события", description)

    @allure.step("Очистить поле 'Краткое описание' (вызываем метод clear())")
    def clear_description(self):
        self.clear_field(self.event_description, "Описание события")

    @allure.step("Заполнить поля с датами и временем")
    def set_event_dates(self, start_date, start_time, end_date, end_time):
        self.populate_field(self.event_date_start, "Дата начала события", start_date)
        self.event_date_start.click()
        self.populate_field(self.event_time_start, "Время начала события", start_time)
        self.event_time_start.click()
        self.populate_field(self.event_date_end, "Дата окончания события", end_date)
        self.event_date_end.click()
        self.populate_field(self.event_time_end, "Время окончания события", end_time)
        self.event_time_end.click()

    @allure.step("Заполнить поле 'Город', проверить выпадающие подсказки и выбрать нужное значение")
    def set_city(self, input_text, result, hint_list):
        self.event_city.scroll_to()
        self.event_city.set_value(input_text)  #Вводим значение для поля
        tooltip_holder = s("div.token-input-dropdown-timepad ul")
        tooltip_holder.should(visible)
        tooltips_all = ss("div.token-input-dropdown-timepad ul li")
        assert len(tooltips_all) > 0, f"Для поля город отстутствуют подсказки"



        value_to_select = None
        for tooltip_el in tooltips_all:
            hint_text = tooltip_el.text
            if hint_text in hint_list:
                hint_list.remove(hint_text)
            if hint_text == result:
                value_to_select = tooltip_el
        assert value_to_select is not None, (f"Необходимое значение {result} для поля город"
                                             f" отстутствует в списке подсказок")
        assert len(hint_list) <= 0, f"В выпадающем списке подсказок отсутствует: {hint_list}"

        value_to_select.click()
        selected_value = s("li.token-input-token-timepad p")
        selected_value.should_have(text(result))


#class TimepadEvent(object):        # NEW_EVENT_PAGE.SET_CITY(TimepadEvent.city_input_text МОС, TimepadEvent.city_result "МОСКВА", TimepadEvent.city_hint_list  "МОСАЛЬСК, МОСКОВСКИЙ")
    #title = 'Интересное событие'
    #description = 'Самое новое событие'
    #category = 'Психология и самопознание'
    #city_input_text = "мос"
    #city_result = "Москва"
    #city_hint_list = ["Мосальск", "Московский", "Мостовской", "Мосты"]

    @allure.step("Заполнить поле 'Категория'")
    def select_category(self, category):
        self.event_category.scroll_to()
        self.event_category.click()
        element_to_select = self.event_category.s(by.xpath(f".//option[text()='{category}']"))
        element_to_select.should(visible)
        element_to_select.click()
        self.event_category.click()
        assert element_to_select.get_attribute('value') == self.event_category.get_attribute("value"), \
            f'Ошибки при заполнении поля: Категория события. Данные: {category}'

    # вспомогательный метод для ввода значения и проверки результата
    def populate_field(self, field, field_name, value):
        field.scroll_to()
        field.set_value(value)
        assert field.get_attribute('value') == value, f'Ошибки при заполнении поля: {field_name}. Данные: {value}'

    # вспомогательный метод для очистки значения и проверки результата
    def clear_field(self, field, field_name):
        field.scroll_to()
        field.clear()
        assert field.get_attribute('value') == "", f'Ошибки при очистки поля: {field_name}.'

    @allure.step("Нажать ссылку 'Дополнительные настройки'")
    def event_settings_click(self):
        self.addition_settings_link.scroll_to()
        self.addition_settings_link.click()
        self.event_settings_block.should(visible)
        self.add_partner_link.should(visible)

    @allure.step("Нажать кнопку 'Опубликовать событие'")
    def create_event(self):
        """
        событие не публикуем
        не все поля заполнены, необходимо добавить проверку после нажатия на кнопку
        проверка что событие создано и произошел переход на другую страницу
        """
        # self.event_submit_button.click()
        pass

class QualityLoginPage(object):
    def __init__(self):
        self.loginField = s('[name="Username"]')
        self.passwordField = s('[name="Password"]')
        self.loginButton = s('[name="button"]')
        self.BranchName = s('#branchTitle')
        self.SelectMenu_Branches = s(by.xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='Статистика'])[1]/following::div[4]"))
        self.SelectBranch = s('[name="branchTitle"]')
        self.ShowBranch = s(by.xpath(u"(.//*[normalize-space(text()) and normalize-space(.)='Avilex test v.2.0'])[1]/following::div[4]"))
        self.ShowSessions = s(by.xpath("//a[text()='Сессии обслуживания']"))
        self.WorkstationField = s(by.xpath("//*[text()='Рабочее место']"
                                           "/ancestor::div[contains(@class, 'col-3-middle')]"))
        self.District = s('#ao')
        self.List = s(by.xpath("//*[@role='menu']"))
        self.ShowButton = s(by.xpath("//*[text()='Показать']/ancestor::button"))
        self.ClearButton = s(by.xpath("//*[text()='Очистить']/ancestor::button"))

        self.TimeSelection = s(by.xpath("//*[text()='Выберите начало промежутка']"
                                               "/ancestor::div[contains(@class, 'col-3-middle')]"))

        self.SelectDate = s(by.xpath("//*[text()='2']/ancestor::button"))
        self.DateChoose = s(by.xpath("//*[text()='Выбрать']/ancestor::button"))
        self.OrganizationList = s(by.xpath("//*@role='gridcell'']/ancestor::div[contains(@class, 'rt-tbody')]"))
        self.FirstElementSessionTable = s(by.xpath("//*[@id='app']/div/div/div/article/div/div[2]/div/div[2]/div/div[1]/div[2]/div[1]"))


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

    @allure.step("Открыть страницу аутентификации qualitycentral.dev.local")
    def open2(self):
        # костыль, чтобы проскочить njinx
        from selene import config
        config.base_url = ""

        open_url('http://qualitycentral.snap.dev.local/web/administration/#/statistics')
        return self

    @allure.step("Перейти на страницу 'Отделения' и ввести Наименование Организации: Проверка что есть в списке ")
    def go_to_branches(self):
        self.SelectMenu_Branches.click()

    @allure.step("Открыть страницу аутентификации qualitycentral.dev.local")
    def open3(self):
        # костыль, чтобы проскочить ninx
     #   from selene import config
      #  config.base_url = ""

        open_url('http://qualitycentral.snap.dev.local/web/administration/#/branchs/')
        return self


##Проверка что данные по значению, веденному в поле, совпадают с БД

    @allure.step("Проверка раздела Сессии обслуживания")
    def sessions_of_the_branch_check(self):
        self.ShowSessions.click()
        self.WorkstationField.click()

    def set_event_dates(self, start_date, start_time, end_date, end_time):
        self.populate_field(self.event_date_start, "Дата начала события", start_date)
        self.event_date_start.click()
        self.populate_field(self.event_time_start, "Время начала события", start_time)
        self.event_time_start.click()
        self.populate_field(self.event_date_end, "Дата окончания события", end_date)
        self.event_date_end.click()
        self.populate_field(self.event_time_end, "Время окончания события", end_time)
        self.event_time_end.click()


    @allure.step("Проверка раздела Сессии обслуживания на заполнение поля Рабочее место и выбор  промежутка времени")
    def select_workstation(self):
        self.WorkstationField.click()
        workstation_list = s(by.xpath("//*[@role='menu']"))
        workstation_list.should(visible)
        value_to_select = workstation_list.s(by.xpath("//*[text()='Рабочая станция 02']/ancestor::*[@role='menuitem']"))
        value_to_select.click()
        workstation_list.should_not(visible)
        self.ShowButton.click()
        self.TimeSelection.click()
        self.SelectDate.click()
        self.DateChoose.click()
        self.DateChoose.click()



    # вспомогательный метод для ввода значения и проверки что эта хуйня работает ваще
    def populate_field(self, field, field_name, value):
        field.scroll_to()
        field.set_value(value)
        assert field.get_attribute('value') == value, f'Ошибки при заполнении поля: {field_name}. Данные: {value}'

     # Типа  для очистки
    def clear_field(self, field, field_name):
        field.scroll_to()
        field.clear()
        assert field.get_attribute('value') == "", f'Ошибки при очистки поля: {field_name}.'


    @allure.step("Заполнить поле 'Отделение'")
    def set_branchName(self, branchname ):
        self.populate_field(self.BranchName, "Отделение", branchname)
        self.ShowButton.click()
        self.ShowBranch.click()

    @allure.step("Очистить поле ''Отделение'' (вызываем метод clear())")
    def clear_BranchName(self):
        self.clear_field(self.BranchName, "'Отделение'")
        self.ShowButton.click()

    @allure.step('Выбор округа из списка по названию: {value}')
    def select_District(self, value):
        self.District.click()
        organization_list = s(by.xpath("//*[@role='menu']"))
        organization_list.should(visible)
        value_to_select = organization_list.s(by.xpath("//*[text()='ТАО']/ancestor::*[@role='menuitem']"))
        value_to_select.click()
        organization_list.should_not(visible)
        self.ShowButton.click()
        self.ClearButton.click()



    @allure.step('Очисти, ну ты знаешь')
    def clear_button(self):
        self.ClearButton.click()

    @allure.step("Заполнить поле 'Наименование', проверить список 'результаты' ")
    def search_organization(self, input_text, hint_list):
        self.BranchName.set_value(input_text)  #Вводим значение для поля
        self.ShowButton.click()
        self.ClearButton.click()

        a = hint_list
        for i, ii in enumerate(a):
            self.BranchName.set_value(a[i])
            self.ShowButton.click()

            field_info = a[i]
            element_to_select = s(by.xpath(f".//*[text()='{field_info}']"))
            b= element_to_select.text
            print (a[i])
            print (b)
            #self.ClearButton.click()
            element_to_select.click()
            self.ShowSessions.click()
            self.TimeSelection.click()
            self.SelectDate.click()
            self.DateChoose.click()
            self.DateChoose.click()
            self.ShowButton.click()
            element_of_time = s(by.xpath("//*[@class='mui-date-picker']/descendant-or-self::*[text()='Выберите начало промежутка']/following-sibling::input"))
            c = element_of_time.get_attribute('value')
            print (c)

            self.ClearButton.click()
            #value_to_select = organization_list.s(by.xpath("//*[text()='1']/ancestor::*[@role='gridcell']"))
            assert field_info == b
            self.FirstElementSessionTable.click()
            self.open3()


    @allure.step("Заполнить поле 'Наименование' неполным наименованием организации, проверить список 'результаты' ")
    def search_organizations(self, input_text, hint_list):
        self.BranchName.set