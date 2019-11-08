import pytest  #очему именно здесь импортируется pytest
from framework.drivers.webdriver_manager import init_driver, close_driver, init_driver_if_not_open, init_new_driver, \
    screenshot_for_allure, screenshot_for_allure_on_fail


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
