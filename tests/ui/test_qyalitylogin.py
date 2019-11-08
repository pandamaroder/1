import allure
import pytest
from framework.resources.test_params.registration_data import BaseAndroidReg, BaseIosReg, INCORRECT_EMAILS, \
    INCORRECT_FIO, INCORRECT_PHONE, INCORRECT_FILES
from framework.resources.test_params.login_data import BaseLogin
from framework.ui_pages.registration_page import RegistrationPage
from framework.ui_pages.registration_page import AfterRegistrationPage

from framework.resources.test_params.registration_data import QualityLogin
from framework.ui_pages.RQualityLoginPage import QualityLoginPage
from datetime import datetime, timedelta



