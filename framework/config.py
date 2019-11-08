import os
from configparser import ConfigParser

import selene
from selene import config

ROOT_PATH = None


class FrameworkConfig(object):

    def __init__(self, pytest_config):
        global ROOT_PATH
        self.pytest_config = pytest_config
        self.root_path = pytest_config.rootdir.strpath
        ROOT_PATH = self.root_path
        self.config_file = f'{self.root_path}/defaults.ini'

        self.config_reader = ConfigParser()
        self.config_reader.read(self.config_file)
        self.configure_selenium()
        self.configure_selene()
        self.configure_allure()

    def configure_selenium(self):
        section = 'selenium'
        self.pytest_config.option.browser = self.get_value(section, 'browser')
        self.pytest_config.option.windows_size = self.get_value(section, 'windows_size')
        self.pytest_config.option.driver_url = self.get_value(section, 'driver_url')
        self.pytest_config.option.browser_version = self.get_value(section, 'browser_version')

    def configure_selene(self):
        section = 'selene'
        selene.config.base_url = self.get_value(section, 'base_url', 'http://sca.snap.dev.local/')         # Нахуя это нужно? ждя конфига селена  - прописка url
        selene.config.timeout = int(self.get_value(section, 'timeout', 10))
        selene.config.poll_during_waits = float(self.get_value(section, 'poll_during_waits', 0.5))
        reports_folder = self.get_value(section, 'reports_folder', 'reports/selene/')
        if not os.path.isabs(reports_folder):
            reports_folder = f'{self.root_path}/{reports_folder}'
        selene.config.reports_folder = reports_folder

    def configure_allure(self):
        section = 'allure'
        allure_dir = self.get_value(section, 'alluredir', argument_name='allure_report_dir')
        if allure_dir is not None:
            if not os.path.isabs(allure_dir):
                allure_dir = f'{self.root_path}/{allure_dir}'
            self.pytest_config.option.allure_report_dir = allure_dir
            self.pytest_config.option.clean_alluredir = self.get_value(section, 'clean-alluredir')

    def get_value(self, conf_section, conf_var, conf_default=None, argument_name=None):
        if argument_name is None:
            argument_name = conf_var
        argument_value = getattr(self.pytest_config.option, argument_name, None)      #CСначала получили значение атрибута объекта pytest_config.option
        if argument_value is not None:                                                # Без всей этой лабуды рботает нормальнононононо
            return argument_value
        return self.config_reader.get(conf_section, conf_var, fallback=conf_default)   # метод Get объекта СоnfigParser https://python-scripts.com/configparser-python-example
                                                                                       # создаем объект ConfigParser и указываем путь к файлу config для чтения.
                                                                                       #Чтобы прочесть опцию в вашем config файле, мы вызываем метод нашего объекта ConfigParser,
        # указываем ему наименование секции и опции. config.get("Settings", "font")

    @staticmethod
    def get_resources_path():
        global ROOT_PATH
        return f'{ROOT_PATH}/framework/resources/'

    def getattr(object, name, default=None):  # known special case of getattr
        """
        getattr(object, name[, default]) -> value

        Get a named attribute from an object; getattr(x, 'y') is equivalent to x.y.
        When a default argument is given, it is returned when the attribute doesn't
        exist; without it, an exception is raised in that case.
        """
        pass
