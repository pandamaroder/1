import os
import sys

import allure
import selene
from allure_commons.types import AttachmentType
from selene import factory, browser
from selenium import webdriver


class Platform(object):
    Windows = 'WINDOWS'
    Linux = 'LINUX'
    MacOS = 'MAC'


class BrowserName(object):
    CHROME = 'chrome'
    FIREFOX = 'firefox'
    IE = 'explorer'


def get_platform_name():
    if 'linux' in sys.platform:
        return Platform.Linux
    if 'darwin' in sys.platform:
        return Platform.MacOS
    return Platform.Windows


def get_drivers_dir():
    return os.path.dirname(os.path.abspath(__file__))


def get_driver_path(browser_name):
    driver_exec = 'chromedriver'
    if browser_name == BrowserName.FIREFOX:
        driver_exec = 'geckodriver'
    if browser_name == BrowserName.IE:
        driver_exec = 'IEDriverServer'

    platform = get_platform_name()
    if platform == Platform.Windows:
        driver_exec = driver_exec + '.exe'
    return f'{get_drivers_dir()}/{platform}/{driver_exec}'


def get_chrome_capabilities():
    desired_capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    desired_capabilities['browserName'] = 'chrome'
    desired_capabilities['browser'] = 'Chrome'
    return desired_capabilities


def get_firefox_capabilities():
    desired_capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
    desired_capabilities['browserName'] = 'firefox'
    desired_capabilities['browser'] = 'Firefox'
    return desired_capabilities


def get_ie_capabilities():
    desired_capabilities = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()
    desired_capabilities['ignoreProtectedModeSettings'] = True
    desired_capabilities['browserName'] = 'internet explorer'
    desired_capabilities['browser'] = 'IE'
    return desired_capabilities


def get_new_local_driver(browser_name):
    if browser_name == BrowserName.FIREFOX:
        driver = webdriver.Firefox(executable_path=get_driver_path(browser_name),
                                   desired_capabilities=get_firefox_capabilities())
    elif browser_name == BrowserName.IE:
        driver = webdriver.Ie(executable_path=get_driver_path(browser_name),
                              desired_capabilities=get_ie_capabilities())
    else:
        driver = webdriver.Chrome(executable_path=get_driver_path(BrowserName.CHROME),
                                  desired_capabilities=get_chrome_capabilities())
    return driver


def get_remote_driver(driver_url, browser_name, browser_version):
    if browser_name == BrowserName.FIREFOX:
        desired_capabilities = get_firefox_capabilities()
    elif browser_name == BrowserName.IE:
        desired_capabilities = get_ie_capabilities()
    else:
        desired_capabilities = get_chrome_capabilities()

    if browser_version is not None:
        desired_capabilities['browser_version'] = browser_version
        desired_capabilities['version'] = browser_version

    return webdriver.Remote(command_executor=driver_url,
                            desired_capabilities=desired_capabilities)


def init_driver(pytest_config):
    browser_name = pytest_config.option.browser
    windows_size = pytest_config.option.windows_size
    driver_url = pytest_config.option.driver_url
    browser_version = pytest_config.option.browser_version

    if driver_url is None:
        driver = get_new_local_driver(browser_name)
    else:
        driver = get_remote_driver(driver_url, browser_name, browser_version)

    if windows_size is None:
        driver.maximize_window()
    else:
        driver.set_window_size(windows_size.split('x')[0], windows_size.split('x')[1])
    selene.browser.set_driver(driver)


def close_driver():
    selene.browser.quit_driver()


def init_driver_if_not_open(pytest_config):
    if not selene.factory.is_driver_still_open(selene.browser.driver()):
        init_driver(pytest_config)


def init_new_driver(pytest_config):
    if selene.factory.is_driver_still_open(selene.browser.driver()):
        close_driver()
    init_driver(pytest_config)


def screenshot_for_allure(request):
    try:
        if request.config.option.allure_report_dir is not None:
            allure.attach(selene.browser.driver().get_screenshot_as_png(),
                          name='screenshot',
                          attachment_type=AttachmentType.PNG)
    except:
        pass


def screenshot_for_allure_on_fail(request):
    try:
        if request.config.option.allure_report_dir is not None:
            allure.attach(selene.browser.driver().find_element_by_tag_name('body').screenshot_as_png,
                          name='screenshot_on_fail',
                          attachment_type=AttachmentType.PNG)
    except:
        pass
