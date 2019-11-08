import tempfile

import os
import datetime
from datetime import timedelta
path = 'C:/Users/o.kukushkina/PycharmProjects/2'
suffix=datetime.datetime.now().strftime("%H%M%S")


def timedelta():
    a = datetime.datetime(2019, 12, 5)
    j=0
    while True:
        b= timedelta(hours=j, minutes=5, seconds=17)
        suffix = a + b
        print(suffix)
        j= j+1
        yield j
    return suffix

i = 0
for filename in os.listdir(path):
    os.rename(os.path.join(path, filename), os.path.join(path, 'device_354_time_' + suffix + str(i) + '.mp4'))
    i = i + 1


i = 0
data = 1
for filename in os.listdir(path):
    with open(filename, 'w') as f:
        f.write(str(data))
        data *= 12
        i = i +1;

res =''
for i in range(1,5):
    file_name = 'file{}.txt'.format(i)
    with open(file_name,'w') as f:
        res += str(i)
        f.write(res)