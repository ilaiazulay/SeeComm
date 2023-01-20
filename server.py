import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
host = '127.0.0.1'
port = 12346

# Bind the socket to a public host, and a port
server_socket.bind((host, port))

# Become a server socket
server_socket.listen(1)

print("Chat Server Started on port " + str(port))

while True:
    # Establish the connection
    client_socket, addr = server_socket.accept()
    print("Got connection from", addr)

    while True:
        # Receive data from the client
        data = client_socket.recv(1024).decode()
        if not data:
            break
        print("Received: ", data)
        # Send data to the client
        client_socket.send(data.encode())
    client_socket.close()
server_socket.close()
