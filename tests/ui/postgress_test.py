from datetime import datetime, timedelta

import allure
import psycopg2
import pytest
from framework.resources.test_params.registration_data import TimepadLogin, TimepadEvent
from framework.ui_pages.registration_page import TimepadPage


@pytest.fixture
def get_city_from_postgres():
    # заглушка при отсутствии БД
    return "мос", "Москва", ["Мосальск", "Московский", "Мостовской", "Мосты"]

    city_input = None
    city_name = None
    hint_list = []

    # параметры подключения
    pgsql_conf = "dbname='quality' user='postgres' password='postgres' host='192.168.10.151' port='5432'"
    #  подключение к БД
    conn = psycopg2.connect(pgsql_conf)
    cur = conn.cursor()

    # выбор города из БД
    city_select = "SELECT city_name FROM cities WHERE length(city_name)>3 ORDER BY random() LIMIT 1"
    cur.execute(city_select)
    if cur.rowcount > 0:
        row = cur.fetchone()
        name = row[0]
        city_name = name
        # значение для поиска города (первые 3 символа названия города в нижнем регистре)
        city_input = city_name[0:3].lower()
    assert isinstance(city_input, str) and len(city_input) == 3, "Не удалось получить город из БД"

    # получиение списка подсказок для вводимого значения (Postgres должна поддерживать ILIKE)
    # либо изменить запрос на основании структуры таблицы и используемых индексов
    hint_select = f"SELECT city_name FROM cities WHERE city_name ILIKE '%{city_input}%' LIMIT 5"
    cur.execute(hint_select)
    for row in cur:
        hint_list.append(row[0])
    conn.close()
    assert len(hint_list) > 0, f"Не удалось получить список подсказок из БД для значения {city_input}"

    return city_input, city_name, hint_list


@pytest.mark.usefixtures('allure_screen')
@allure.feature('Timepad авторизация, создание нового собятия')
class TestTimepad:

    @allure.story('Проверка авторизации')
    @allure.testcase('https://google.com/', name='Ссылка на тест-кейс')
    def test_timepad(self, get_city_from_postgres):
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
        # Проверить что авторизовались успешно (появилась ссылка на личный кабинет)
        page.check_auth(TimepadLogin.user_name)
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
        new_event_page.set_city(get_city_from_postgres[0], get_city_from_postgres[1], get_city_from_postgres[2])
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


from clickhouse_driver import Client
client=Client(host='192.168.10.86',user='avx',password='ksMsw1w5fE',port=8123, database= 'schoolwifi_facts')
print(client.execute('select * from user_login limit 5'))