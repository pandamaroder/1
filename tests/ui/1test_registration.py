import allure
import pytest
from framework.resources.test_params.registration_data import BaseAndroidReg, BaseIosReg, INCORRECT_EMAILS, \
    INCORRECT_FIO, INCORRECT_PHONE, INCORRECT_FILES
from framework.resources.test_params.login_data import BaseLogin
from framework.ui_pages.registration_page import RegistrationPage
from framework.ui_pages.registration_page import AfterRegistrationPage

from framework.resources.test_params.registration_data import TimepadLogin, TimepadEvent, QualityLogin, QualityParams
from framework.ui_pages.registration_page import TimepadPage, QualityLoginPage
from datetime import datetime, timedelta

@pytest.mark.positive
@pytest.mark.usefixtures('allure_screen')
@allure.feature('smd.mos.ru Регистрация')
class TestRegistrationForm:

    @allure.story('Проверка формы регистрации при заполнении валидными данными')
    def test_registration(self):
        page = RegistrationPage().open()
        page.select_organization(BaseAndroidReg.organization)
        page.populate_user_name(BaseAndroidReg.fio)
        page.populate_email(BaseAndroidReg.email)
        page.populate_phone(BaseAndroidReg.phone)
        page.select_mobile_os(BaseAndroidReg.mobile_os)
        page.populate_google_play(BaseAndroidReg.email)
        page.upload_scan_image(BaseAndroidReg.scan_image)
        page.assert_page_errors()

    @allure.story('Проверка формы регистрации при заполнении валидными данными, ручное создание логина')
    def test_registration_login(self):
        page = RegistrationPage().open()
        page.select_organization(BaseAndroidReg.organization)
        page.populate_user_name(BaseAndroidReg.fio)
        page.populate_email(BaseAndroidReg.email)
        page.populate_phone(BaseAndroidReg.phone)
        page.select_mobile_os(BaseAndroidReg.mobile_os)
        page.populate_google_play(BaseAndroidReg.email)
        page.populate_login(BaseAndroidReg.login)
        page.upload_scan_image(BaseAndroidReg.scan_image)
        page.assert_page_errors()

    @allure.story('Проверка формы регистрации при заполнении валидными данными, iOS, ручное создание логина')
    def test_registration_ios_login(self):
        page = RegistrationPage().open()
        page.select_organization(BaseIosReg.organization)
        page.populate_user_name(BaseIosReg.fio)
        page.populate_email(BaseIosReg.email)
        page.populate_phone(BaseIosReg.phone)
        page.select_mobile_os(BaseIosReg.mobile_os)
        page.google_play_field_disabled_check()
        page.populate_login(BaseIosReg.login)
        page.upload_scan_image(BaseIosReg.scan_image)
        page.assert_page_errors()


@pytest.mark.negative
@pytest.mark.usefixtures('allure_screen')
@allure.feature('smd.mos.ru Регистрация: валидация сообщений об ошибках')
class TestRegistrationFieldsAlert:

    @allure.story('Проверка поля Организация')
    def test_organization_field(self):
        page = RegistrationPage().open()
        page.populate_none_exist_organization('OOO "Рога и Копыта"')

    @pytest.mark.parametrize('name', INCORRECT_FIO)
    @allure.story('Проверка поля ФИО: {name}')
    def test_fio_field(self, name):
        page = RegistrationPage().open()
        assert not page.populate_user_name(name, assert_on_fail=False), f'Поле ФИО заполнено без ошибок данными: {name}'

    @pytest.mark.parametrize('email', INCORRECT_EMAILS)
    @allure.story('Проверка поля email: {email}')
    def test_email_field(self, email):
        page = RegistrationPage().open()
        assert not page.populate_email(email, assert_on_fail=False), f'Поле email заполнено без ошибок данными: {email}'

    @pytest.mark.parametrize('phone', INCORRECT_PHONE)
    @allure.story('Проверка поля телефон: {phone}')
    def test_phone_field(self, phone):
        page = RegistrationPage().open()
        assert not page.populate_phone(phone,
                                       assert_on_fail=False), f'Поле телефон заполнено без ошибок данными: {phone}'

    @pytest.mark.parametrize('email', INCORRECT_EMAILS)
    @allure.story('Проверка поля Google Play: {email}')
    def test_google_play_field(self, email):
        page = RegistrationPage().open()
        page.select_mobile_os('Android')
        assert not page.populate_google_play(email, assert_on_fail=False),\
            f'Поле Google Play заполнено без ошибок данными: {email}'

    @pytest.mark.parametrize('file', INCORRECT_FILES)
    @allure.story('Проверка загрузки файла: {file}')
    def test_upload_scan_field(self, file):
        page = RegistrationPage().open()
        assert not page.upload_scan_image(file, assert_on_fail=False), f'Файл добавлен без ошибок: {file}'

    @pytest.mark.usefixtures('allure_screen')
    @allure.feature('smd.mos.ru Регистрация')
    class TestAdministrationForm:

        @allure.story('Проверка формы регистрации при заполghghghи')
        def test_administration(self):
            page = AfterRegistrationPage()
            page.open()
            page.login(BaseLogin.login, BaseLogin.password)
            page.organization2_populate(BaseIosReg.organization2)
            page.open2()
##Open page after login


@pytest.mark.negative1
@pytest.mark.usefixtures('allure_screen')
@allure.feature('Timepad авторизация, создание нового собятия')
class TestTimepad:

    @allure.story('Проверка авторизации')
    @allure.testcase('https://google.com/', name='Ссылка на тест-кейс')
    def test_timepad(self):
        """
        Открыть страницу https://timepad.ru
        Нажать кнопку 'Войти'
        Заполнить форму авторизации
        Проверить что авторизовались успешно (появилась ссылка на личный кабинет)
        Нажать кнопку 'Опубликовать событие'
        Заполнить поле 'Название'
        Заполнить поле 'Краткое описание'
        Заполнить поле 'Дата начала' (завтра)
        Заполнить поле 'Время начала' (08:00)
        Заполнить поле 'Дата окончания' (завтра + 1 неделя)
        Заполнить поле 'Время окончания' (22:00)
        Заполнить поле 'Город' (ввести значение 'мос')
            проверить что в выпадающем списке содержаться подсказки (Москва, Мосальск, Московский, Мостовской, Мосты)
            нажать на подсказку 'Москва'
            проверить что выбранное значение появилось в поле
        Заполнить поле 'Категория' (Выбрать из списка 'Психология и самопознание')
        Очистить поле 'Название' (вариант #1 вводим пустое значение)
        Очистить поле 'Краткое описание' (вариант #2 вызываем метод clear())
        Кликаем на ссылку 'Дополнительные настройки' проверяем видимость дочерних элементов
        Нажимаем кнопку 'Продолжить' (не активно)
        """

        page = TimepadPage()
        # Открыть страницу https://timepad.ru
        page.open()
        #  Нажать кнопку 'Войти' и заполнить форму авторизации
        page.login(TimepadLogin.email, TimepadLogin.password)
        print(TimepadLogin.email, TimepadLogin.password)
        # Проверить что авторизовались успешно (появилась ссылка на личный кабинет)
        page.check_auth(TimepadLogin.user_name)
        print(page.check_auth)
        # Нажать кнопку 'Опубликовать событие'
        new_event_page = page.create_event_button_click()
        # Заполнить поле 'Название'
        new_event_page.set_title(TimepadEvent.title)
        # Заполнить поле 'Краткое описание'
        new_event_page.set_description(TimepadEvent.description)
        # Сформировать дату и время для начала и окончания события
        current_time = datetime.now()
        date_start = (current_time + timedelta(days=1)).strftime("%d.%m.%Y")
        time_start = "08:00"
        date_end = (current_time + timedelta(days=8)).strftime("%d.%m.%Y")
        time_end = "22:00"
        # Заполнить поля с датами и временем
        new_event_page.set_event_dates(date_start, time_start, date_end, time_end)
        # Заполнить поле 'Город' (ввести значение 'мос')
        #     проверить что в выпадающем списке содержаться подсказки (Москва, Мосальск, Московский, Мостовской, Мосты)
        #     нажать на подсказку 'Москва'
        #     проверить что выбранное значение появилось в поле
        new_event_page.set_city(TimepadEvent.city_input_value, TimepadEvent.city_result, TimepadEvent.city_hint_list)
        # Заполнить поле 'Категория' (Выбрать из списка 'Психология и самопознание')
        new_event_page.select_category(TimepadEvent.category)

        # Очистить поле 'Название' (вариант #1 вводим пустое значение)
        new_event_page.set_title("")
        # Очистить поле 'Краткое описание' (вариант #2 вызываем метод clear())
        new_event_page.clear_description()
        # Кликаем на ссылку 'Дополнительные настройки'
        new_event_page.event_settings_click()
        # Нажимаем кнопку 'Продолжить' (не активно)
        new_event_page.create_event()



#@pytest.mark.usefixtures('allure_screen')
#@allure.feature('QUALITY GLOBAL')
class TestQuality1:

    #@allure.story('Проверка авторизации')
    #@allure.testcase('http://qualitycentral.dev.local', name='Ссылка на тест-кейс в тест-линке')
    def test_quality(self):
        """
        Открыть страницу http://qualitycentral.dev.local
        Нажать кнопку 'Войти'
        Заполнить форму авторизации
        Проверить что авторизовались успешно (перекинуло на nginx)

        """

        page = QualityLoginPage()
        # Открыть страницу и не наебнуться
        page.open()
        #  Заполнить форму авторизации и Нажать кнопку 'Войти' и ахуеть
        page.login(QualityLogin.login, QualityLogin.password)
        print(QualityLogin.login, QualityLogin.password)
        # Проверить что авторизовались успешно (появилась cтраница NGINX)
        page.open2()
        page.go_to_branches()
                # Проверка на поиск отделения
        #page.set_organization(input_text, hint_list)
        page.set_branchName(QualityParams.description)
        page.sessions_of_the_branch_check()
        page.select_workstation()
        page.open3()
        #page.clear_button()
        #page.clear_BranchName()
        page.select_District(QualityParams.District)

