import pytest
import requests
import random


urls = ["https://ya.ru", "https://google.com", "https://mail.ru"]
headers = [{"Content-type": "application/json"}, {"Content-type": "text/html"}, {}]
pairs = [(url, header) for url in urls for header in headers]


@pytest.fixture(params= pairs)
def response(request):
    print ("\nI'm first argument of pairsrequest.param {}\n".format(request.param))
    print(request.param[0])
    print(request.param[1])
    return requests.get(request.param[0], headers= request.param[1])



@pytest.mark.usefixtures("response")
def test_urls(response):
    assert response.status_code == 200



#Файл conftest в структуре сonftest.py <-> test_api.py

class APIClient:
    headers = {"Some_Header": "someheader"}

    def __init__(self, address= 'https://ya.ru'):
        self.address = address

    def do_get(self, endpoint, verify_ssl= False):
        url = "/".join([self.address, endpoint])
        return requests.get(url, headers=self.headers, verify= verify_ssl)

    def do_post(self, endpoint, data=None, verify_ssl= False):
        url = "/".join([self.address, endpoint])
        headers= self.headers
        headers["Content-type"] = "application/json"
        return requests.post(url, data, headers=headers, verify = verify_ssl)

    def pytest_addoption(parser):
        parser.addoption('--address', action= 'store', default= 'http://localhost:7070')


@pytest.fixture
def client(request):
    return APIClient(request.config.getoption("--address"))


endpoints = ["endpoint1", "endpoint2"]
post_endpoints_without_data= ["endpoint1", "endpoint2"]

#@pytest.mark.parametrize("endpoint", endpoints)
#def test_endpoints_encoding(request, client, endpoint):
    #print(request.config.getoption('--address'))
    #
#assert type(request.config.getoption('--address')) is str


dyn_args = [random.random() for x in range(10)]

@pytest.mark.parametrize("x", dyn_args)
def test_func(x):
    print(x)

