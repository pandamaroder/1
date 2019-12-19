import requests
import json
import jsonpath

url = "https://reqres.in/api/users"
headerdata = {'Server':'nginx/1.17.2', 'Content-Type':'application/json', 'Connection':'keep-alive'}


file = open("C:/Users/o.kukushkina/PycharmProjects/smd_mos4/framework/resources/test_params/NewSession.json", 'r')
json_input = file.read()

request_json = json.loads(json_input)
headerdata = {'Server':'nginx/1.17.2', 'Content-Type':'application/json', 'Connection':'keep-alive', 'Transfer-Encoding':'chunked'}

print(request_json)

a = requests.post(url, request_json)
print(a.text)
print (a.status_code)
print (a.headers.get('Content-Length'))

response_json = json.loads(a.text)
print(response_json)

url = "https://requests.in/api/users?page=2"

response = requests.get(url)
json_response = json.loads(response.text)

pages = jsonpath.jsonpath(json_response, 'total_pages')
assert pages[0] == 5


for i in range(0,3):
    data[0].first_name
    first_name = jsonpath.jsonpath(json_response, 'data['+str(i)+']')


a = requests.post(url, request_json)
print(a.text)
print(a.status_code)
print(a.headers)



