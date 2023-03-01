import socket
import threading

HOST = '127.0.0.2'
PORT = 9090

# Get the local IP address of the machine
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("0.0.0.0", 80))
local_ip = s.getsockname()[0]
s.close()

print("Local IP address:", local_ip)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((local_ip, PORT))

server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break


def receive():
    while True:
        client, address = server.accept()
        print(f"connected with {str(address)}!")

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)

        nicknames.append(nickname)
        clients.append(client)

        print(f"nickname of the client is {nickname}")
        broadcast(f"{nickname} connected to the server!\n".encode('utf-8'))
        client.send("Connected to the server".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server running...")
receive()















