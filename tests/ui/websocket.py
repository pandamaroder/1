import socket

sock = socket.socket()
sock.connect(('192.168.10.129', 30602))
sock.send(b'hello, world!')

data = sock.recv(1024)
sock.close()
print(data)