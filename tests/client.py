import socket

soc = socket.socket()
soc.connect(('localhost', 12333))
while True:
    mess = input(":: ")
    soc.send(bytes(mess, 'utf-8'))
    print(soc.recv(1024).decode())

soc.close()