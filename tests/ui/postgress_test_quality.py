from datetime import datetime, timedelta

import allure
import psycopg2
import pytest
from framework.resources.test_params.registration_data import QualityLogin, QualityParams
from framework.ui_pages.registration_page import TimepadPage, QualityLoginPage
from delayed_assert import expect, assert_expectations


@pytest.fixture
def get_city_from_postgres():
    # заглушка при отсутствии БД
    #return "мос", "Москва", ["Мосальск", "Московский", "Мостовской", "Мосты"]

    organization_input = None
    organization_name = None
    hint_list = []

    # параметры подключения
    pgsql_conf = "dbname='quality' user='postgres' password='postgres' host='192.168.10.151' port='5432'"
    #  подключение к БД
    conn = psycopg2.connect(pgsql_conf)
    cur = conn.cursor()
    name = 'Avilex'
    # выбор города из БД
    organization_select = "SELECT name FROM service.branch WHERE id = 218"
    cur.execute(organization_select)
    if cur.rowcount > 0:

        row = cur.fetchone()
        organization_name = row[0]
        # значение для поиска города (первые 3 символа названия города в нижнем регистре)
        organization_input = organization_name.lower()
        organization_input = organization_name[0:22].lower()
    #assert isinstance(organization_input, str) and len(organization_input) == 49, "Не удалось получить город из БД"

    # получиение списка подсказок для вводимого значения (Postgres должна поддерживать ILIKE)
    # либо изменить запрос на основании структуры таблицы и используемых индексов
    hint_select = f"SELECT name FROM service.branch WHERE name ILIKE '%{organization_input}%' LIMIT 5"
    cur.execute(hint_select)
    for row in cur:
        hint_list.append(row[0])
    conn.close()
    assert len(hint_list) > 0, f"Не удалось получить список подсказок из БД для значения {organization_input}"

    return organization_input,  hint_list


def test_should_pass():
    expect(1 == 1, 'one is one')
    assert_expectations()




@pytest.mark.usefixtures('allure_screen')
@allure.feature('Timepad авторизация, создание нового собятия')
class TestQualityPage:

    @allure.story('Проверка поиска организации')
    @allure.testcase('http://qualitycentral.snap.dev.local/', name='Ссылка на тест-кейс')
    def test_qyality(self, get_city_from_postgres):

        page = QualityLoginPage()
        # Открыть страницу и не наебнуться
        page.open()
        #  Заполнить форму авторизации и Нажать кнопку 'Войти' и ахуеть
        page.login(QualityLogin.login, QualityLogin.password)
        print(QualityLogin.login, QualityLogin.password)
        # Проверить что авторизовались успешно (появилась cтраница NGINX)
        page.open3()
        # Заполнить поле 'наименование' (ввести значение 'мос')
        #     проверить что в выпадающем списке содержаться подсказки (Москва, Мосальск, Московский, Мостовской, Мосты)
        #     нажать на подсказку 'Москва'
        #     проверить что выбранное значение появилось в поле
        page.search_organization(get_city_from_postgres[0],get_city_from_postgres[1])
