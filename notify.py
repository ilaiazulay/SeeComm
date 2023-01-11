import socket
import threading

class Patient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))

    def notify_workers(self):
        self.client.send("Patient needs assistance!".encode())
        print("Notified workers.")

    def close(self):
        self.client.close()

class Worker:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.notification_flag = 0

    def start(self):
        worker_thread = threading.Thread(target=self.work)
        worker_thread.start()

    def work(self):
        while True:
            client_socket, client_address = self.server.accept()
            notification = client_socket.recv(1024).decode()
            if notification == "Patient needs assistance!":
                print("Received notification from {}: {}".format(client_address, notification))
                self.notification_flag = 1
            client_socket.close()

if __name__ == "__main__":
    worker = Worker("localhost", 55555)
    worker.start()

    # Patient can notify the workers by creating an instance of the Patient class
    # and calling the notify_workers method
    patient = Patient("localhost", 55555)
    patient.notify_workers()
    patient.close()
