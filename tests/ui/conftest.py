import pytest  # именно здесь импортируется pytest для реализации фикстур
from framework.drivers.webdriver_manager import init_driver, close_driver, init_driver_if_not_open, init_new_driver, \
    screenshot_for_allure, screenshot_for_allure_on_fail
import psycopg2


@pytest.fixture(scope='session', autouse=True)
def setup_driver(request):
    init_driver(request.config)
    request.addfinalizer(close_driver)


@pytest.fixture(autouse=True)
def setup_driver_if_not_open(request):
    init_driver_if_not_open(request.config)


@pytest.fixture()
def re_init_driver(request):
    init_new_driver(request.config)


@pytest.yield_fixture()
def allure_screen(request):
    yield
    screenshot_for_allure(request)


def pytest_exception_interact(node, call, report):
    screenshot_for_allure_on_fail(node)


@pytest.fixture
def get_city_from_postgres():
    # заглушка при отсутствии БД
    #return "мос", "Москва", ["Мосальск", "Московский", "Мостовской", "Мосты"]

    organization_input = None
    organization_name = None
    hint_list = []

    # параметры подключения
    pgsql_conf = "dbname='quality' user='postgres' password='postgres' host='192.168.10.171' port='5432'"
    #  подключение к БД
    conn = psycopg2.connect(pgsql_conf)
    cur = conn.cursor()
    name = 'Avilex'
    # выбор города из БД
    organization_select = "SELECT name FROM service.branch WHERE id = 377 or id = 74"
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
