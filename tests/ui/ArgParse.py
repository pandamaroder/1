import argparse

parser = argparse.ArgumentParser()

parser.add_argument('-s', action='store', dest='simple_value', help='Store a simple value')

parser.add_argument('-c', action='store_const', dest='constant_value', const='value-to-store', help='Store a constant value')

parser.add_argument('-t', action='store_false', default=True, dest='boolean_switch', help='Set a switch to true')

parser.add_argument('-a', action='append', dest='collection', default=[], help='Add repeated values to a list')

results = parser.parse_args()
print('simple_value    =', results.simple_value)
print('constant_value  =', results.constant_value)
print('boolean_switch  =', results.boolean_switch)
print('collection   =', results.collection)


x = iter([1, 2, 3])
print(dir(x))


import gzip, bz2
from pathlib import Path

def gen_open(paths):
    for path in paths:
        if path.suffix == '.gz':
            yield gzip.open(path, 'rt')
        elif path.suffix == '.bz2':
            yield bz2.open(path, 'rt')
        else:
            yield open(path, 'rt')

def gen_cat(sources):
    for src in sources:
        for item in src:
            yield item

lognames = Path('/usr/www').rglob("access-log*")
logfiles = gen_open(lognames)
loglines = gen_cat(logfiles)
#logfiles.__next__()

#ReadFileGenerator readfile-generator.py  38:34

with open("access-log") as wwwlog:
    bytecolumn = (line.rsplit(None,1)[1] for line in wwwlog)
    bytes_sent = (int(x) for x in bytecolumn if x != '-')
    print("Total", sum(bytes_sent))

#example3-rwb

f = open('workfile', 'rb+')
f.write(b'0123456789abcdef')
f.seek(10)

#fileobject 33:22

with open("mynewtextfile.txt", "w+") as f:
    f.write("Otus we are learning\nOtus we are learning python\nOtus we are learning pythom")
    f.seek(0)
    print(f.read())
    print("Is readable:", f.readable())
    print("Is writable:", f.writable())
    print("fghgfhfghfgh:", f.fileno())
    print("fghfghgf:", f.isatty())
    f.truncate(5)
    f.flush()
    f.seek(0)
    print(f.read())
