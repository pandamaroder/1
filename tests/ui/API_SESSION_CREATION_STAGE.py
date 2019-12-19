import requests
import json

url = "http://qualitylocal.stage.dev.local/api/sessions/fromremote"

file = open("C:/Users/o.kukushkina/PycharmProjects/smd_mos4/framework/resources/test_params/NewSession.json", 'r')
json_input = file.read()
print (json_input)
headerdata = {'Server':'nginx/1.17.2', 'Content-Type':'application/json', 'Connection':'keep-alive'}
SESSION = requests.post(url, json_input, headers=headerdata)
print(SESSION.text)
print (SESSION.status_code)



url2 = "http://qualitylocal.stage.dev.local/api/sessions/fromremote/stop"

file2 = open("C:/Users/o.kukushkina/PycharmProjects/smd_mos4/framework/resources/test_params/SessionStop.json", 'r')
json_input2 = file2.read()
print (json_input2)
headerdata = {'Server':'nginx/1.17.2', 'Content-Type':'application/json', 'Connection':'keep-alive'}
SESSION = requests.post(url2, json_input2, headers=headerdata)
print(SESSION.text)
print (SESSION.status_code)
print (json_input2)
print (json_input)

#url3 = "http://quality.snap.dev.local/update/api/updatechannels/update-pads-channel"
#SESSION = requests.put(url3, 'cb09af1d-2917-4d64-8af9-c42a574fdc9d')
#print(SESSION.text)

url4 =  "http://qualitylocal.stage.dev.local/update/api/updatechannels/update-channel/153"
SESSION = requests.get(url4)
print(SESSION.text)
print (SESSION.status_code)