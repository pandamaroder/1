import tempfile

for i in range(1,5):
    tf = tempfile.NamedTemporaryFile(prefix = 'device_359_time_', dir = 'C:/Users/o.kukushkina/PycharmProjects/2', delete=False)
    print(tf.name)

import os
import datetime
from datetime import timedelta

path = 'C:/Users/o.kukushkina/PycharmProjects/2'

