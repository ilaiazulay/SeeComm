import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QCursor
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5 import uic
import socket
import time

class ChatThread(QtCore.QThread):
    messageReceived = QtCore.pyqtSignal(str)

    def __init__(self, host='127.0.0.1', port=12346, role="patient"):
        super(ChatThread, self).__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        self.role = role

    def run(self):
        self.send_message_to_server(self.role) # send client role to server
        while True:
            message = self.receive_message_from_server()
            self.messageReceived.emit(message)

    def send_message_to_server(self, message):
        self.s.send(bytes(message, 'utf-8'))

    def receive_message_from_server(self):
        data = self.s.recv(1024)
        return data.decode()


class patientChatPage(QMainWindow):
    def __init__(self):
        super(patientChatPage, self).__init__()
        uic.loadUi("../UI/chat_page.ui", self)
        self.input_box.installEventFilter(self)
        self.send_button.clicked.connect(self.sendMessage)
        self.chat_thread = ChatThread(role="patient") # pass client role
        self.chat_thread.messageReceived.connect(self.displayMessage)
        self.chat_thread.start()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj is self.input_box:
            if event.key() == QtCore.Qt.Key_Return and self.input_box.hasFocus():
                self.sendMessage()
        return False

    def sendMessage(self):
        message = self.input_box.toPlainText()
        self.chat_thread.send_message_to_server(message)
        self.input_box.clear()

    def displayMessage(self, message):
        role, message = message.split(" : ")
        if role == self.chat_thread.role:
            message = "you: " + message
        self.output_box.insertPlainText(message + '\n')

class stuffMemberChatPage(QMainWindow):
    def __init__(self):
        super(stuffMemberChatPage, self).__init__()
        uic.loadUi("../UI/chat_page.ui", self)
        self.input_box.installEventFilter(self)
        self.send_button.clicked.connect(self.sendMessage)
        self.chat_thread = ChatThread(role="patient") # pass client role
        self.chat_thread.messageReceived.connect(self.displayMessage)
        self.chat_thread.start()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj is self.input_box:
            if event.key() == QtCore.Qt.Key_Return and self.input_box.hasFocus():
                self.sendMessage()
        return False

    def sendMessage(self):
        message = self.input_box.toPlainText()
        self.chat_thread.send_message_to_server(message)
        self.input_box.clear()

    def displayMessage(self, message):
        role, message = message.split(" : ")
        if role == self.chat_thread.role:
            message = "you: " + message
        self.output_box.insertPlainText(message + '\n')


if __name__ == "__main__":
    # exec(open("../server.py").read())
    app = QtWidgets.QApplication(sys.argv)
    window = patientChatPage()
    window.show()
    sys.exit(app.exec_())
