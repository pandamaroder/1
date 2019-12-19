
import json
data = {'jsonKey': 'jsonValue',"title": "hello world"}

print (json.dumps(data))
a = str(data)
print (a)
print (type(a))

b = a[0:5]
print(b)

## Cначала прочитали сторку
## потом json.pop  -  убираем из источника
# json.dump того что взяли из json
## конвертирование в строку
## replace элементов
## потом очистка данных
## потом замена этого элемента во всей строке




