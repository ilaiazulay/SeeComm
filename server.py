import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
host = '127.0.0.1'
port = 12347

# Bind the socket to a public host, and a port
server_socket.bind((host, port))

# Become a server socket
server_socket.listen(1)

print("Chat Server Started on port " + str(port))

while True:
    # Establish the connection
    client_socket, addr = server_socket.accept()
    client_id = client_socket.recv(1024).decode()
    if client_id == "patient":
        print("Connected patient:", addr)
    else:
        print("Connected staff member")

    while True:
        # Receive data from the client
        data = client_socket.recv(1024).decode()
        if not data:
            break
        message = client_id + " : " + data
        print("Received: ", message)
        # Send data to the client
        client_socket.send(message.encode())
    client_socket.close()
