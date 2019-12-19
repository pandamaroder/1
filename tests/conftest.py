from framework.config import FrameworkConfig


def pytest_addoption(parser):
    parser.addoption('--base_url', action='store', help='Base url')
    parser.addoption('--browser', action='store', help='Browser name. Default: chrome')
    parser.addoption('--windows_size', action='store', help='Window size. Default: full screen')
    parser.addoption('--driver_url', action='store', help='Selenoid/selenium grid url')
    parser.addoption('--browser_version', action='store', help='Browser version. Use in selenoid/selenium grid')



# import pytest
#def pytest_addoption(parser):
    #parser.addoption(
       # "--runslow", action="store_true", default=False, help="run slow tests"


def pytest_configure(config):
    """" * **pytest_configure** - Выполняется во время конфигурирования Pytest и его плагинов:

    - Выполняет настройку фреймворка на основе параметров командной строки и файла **./defaults.ini**
    - Настройку фреймворка производит класс **FrameworkConfig** из модуля **./framework/config.py**
    - Параметры командной строки имеют больший приоритет """
    FrameworkConfig(config)
