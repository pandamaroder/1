from framework.config import FrameworkConfig


class BaseIosReg(object):
    organization = 'Академия лепки DECO'
    fio = 'Иванов Иван Иванович'
    email = 'test@test.ru'
    phone = '+7(987)654-32-10'
    mobile_os = 'iOS'
    login = 'test12345'
    scan_image = FrameworkConfig.get_resources_path() + 'img/scan.jpg'
    organization2 = "ИП 'Ивлива М.Н.'"
    orgunit = "Национальная федерация флорбола России"


class BaseAndroidReg(BaseIosReg):
    organization = 'Академия лепки DECO'
    mobile_os = 'Android'


INCORRECT_EMAILS = [
    'Василий',
    'г. Москва, ул. Ленина 1',
    'test@test.ru$',
    'test@test._u',
    'test.test@@test.ru',
    'test@домен._u',
    'cococo@домен.рф',
]

INCORRECT_FIO = [
    'Василий',
    'Инокентий Sбруев',
    'Петр1',
]

INCORRECT_PHONE = [
    'Три пять семь',
    '89876543210',
    '+6(987)654-32-10',
]

INCORRECT_FILES = [
    FrameworkConfig.get_resources_path() + 'img/empty.txt',
]


class TimepadLogin(object):
    email = 'maks-sn@yandex.ru'
    password = 'qwerty123456'
    user_name = 'maks-sn'


class TimepadEvent(object):
    title = 'Интересное событие'
    description = 'Самое новое событие'
    category = 'Психология и самопознание'
    city_input_value = "мос"
    city_result = "Москва"
    city_hint_list = ["Мосальск", "Московский", "Мостовской", "Мосты"]


class QualityLogin(object):
    login = 'SuperAdministrator'
    password = '123qwe'

class QualityParams(object):
    description = 'Avilex'
    District = 'TAO'