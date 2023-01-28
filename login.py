import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QCursor
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5 import uic
import notify
from PyQt5.QtCore import QTimer
import socket

# Landing page
class landingPage(QMainWindow):
    def __init__(self):
        super(landingPage, self).__init__()
        uic.loadUi("./UI/first_page.ui", self)
        self.chat.clicked.connect(self.chat_function)
        self.staff_login.clicked.connect(self.login_function)
        self.information.clicked.connect(self.information_function)

    def chat_function(self):
        # send notification to the workers
        patient = notify.Patient("localhost", 12346)
        patient.notify_workers()
        patient.close()
        create_waiting_widget = chatWaitingWidget()
        widget.addWidget(create_waiting_widget)
        widget.setCurrentIndex(widget.currentIndex()+1)


    def login_function(self):
        create_login_page = loginPage()
        widget.addWidget(create_login_page)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def information_function(self):
        create_information_page = informationPage()
        widget.addWidget(create_information_page)
        widget.setCurrentIndex(widget.currentIndex()+1)

# Login page
class loginPage(QMainWindow):
    def __init__(self):
        super(loginPage, self).__init__()
        uic.loadUi("./UI/login_page.ui", self)
        self.verification_message.setHidden(True)
        self.back_button.clicked.connect(self.back_function)
        self.UN = self.username.text()
        self.PASS = self.password.text()
        self.username.installEventFilter(self)
        self.password.installEventFilter(self)
        # self.login.clicked.connect(self.staff_page_function)
        self.login.clicked.connect(self.verification)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and (obj is self.username or self.password):
            if event.key() == QtCore.Qt.Key_Return and (self.username.hasFocus() or self.password.hasFocus()):
                self.verification()
                pass
        return False

    def back_function(self):
        widget.removeWidget(widget.currentWidget())

    def staff_page_function(self):
        create_staff_page = staffPage()
        widget.addWidget(create_staff_page)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def verification(self):
        username = self.username.text()
        password = self.password.text()
        if username != "admin" or password != "admin":
            self.verification_message.setHidden(False)
        else:
            self.login.clicked.connect(self.staff_page_function)
            pass

# staff page
class staffPage(QMainWindow):
    def __init__(self):
        super(staffPage, self).__init__()
        uic.loadUi("./UI/staff_page.ui", self)
        self.worker = notify.Worker("localhost", 12346)
        self.worker.start()
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateChatRequest)
        self.timer.start(2000)  # 1000 ms = 1 second
        self.answer.clicked.connect(self.enterChat)

    def updateChatRequest(self):

        if self.worker.notification_flag == 1:
            self.patient_waiting_number.setText(str(1))
            self.answer.clicked.connect(self.enterChat)

    def enterChat(self):
        create_stuff_member_chat_page = stuffMemberChatPage()
        widget.addWidget(create_stuff_member_chat_page)
        widget.setCurrentIndex(widget.currentIndex()+1)

class ChatThread(QtCore.QThread):
    messageReceived = QtCore.pyqtSignal(str)
    def run(self):
        while True:
            message = self.receive_message_from_server()
            self.messageReceived.emit(message)

    def receive_message_from_server(self):
        # This is a placeholder function that simulates receiving a message from a server
        return "Server: Hello, how are you?"


class chatPage(QMainWindow):
    def __init__(self):
        super(chatPage, self).__init__()
        uic.loadUi("./UI/chat_page.ui", self)
        self.input_box.returnPressed.connect(self.sendMessage)
        self.send_button.clicked.connect(self.sendMessage)
        self.chat_thread = ChatThread()
        self.chat_thread.messageReceived.connect(self.displayMessage)
        self.chat_thread.start()

class chatWaitingWidget(QWidget):
    def __init__(self):
        super(chatWaitingWidget, self).__init__()
        uic.loadUi("./UI/chat_wait_widget.ui", self)
        # self.connecting_label.setText(str(0))
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateLabel)
        self.timer.start(1000)  # 1000 ms = 1 second
        self.text_variation = 0
        self.cancel_button.clicked.connect(self.back_function)

    def back_function(self):
        widget.removeWidget(widget.currentWidget())
    def updateLabel(self):
        if self.text_variation % 3 == 0:
            self.label.setText("Connecting to the chat, Please wait.")
        if self.text_variation % 3 == 1:
            self.label.setText("Connecting to the chat, Please wait..")
        if self.text_variation % 3 == 2:
            self.label.setText("Connecting to the chat, Please wait...")
        self.text_variation = (self.text_variation + 1) % 3
        # check if staff member entered the chat
        message = self.chat_thread.receive_message_from_server()
        if message == "Connected staff member":
            create_patient_chat_page = patientChatPage()
            widget.addWidget(create_patient_chat_page)
            widget.setCurrentIndex(widget.currentIndex()+1)


class ChatThread(QtCore.QThread):
    messageReceived = QtCore.pyqtSignal(str)

    def __init__(self, host='127.0.0.1', port=12347, role="patient"):
        super(ChatThread, self).__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        self.role = role

    def run(self):
        self.send_message_to_server(self.role)  # send client role to server
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
        uic.loadUi("./UI/chat_page.ui", self)
        self.input_box.installEventFilter(self)
        self.send_button.clicked.connect(self.sendMessage)
        self.chat_thread = ChatThread(role="patient")  # pass client role
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
        uic.loadUi("./UI/chat_page.ui", self)
        self.input_box.installEventFilter(self)
        self.send_button.clicked.connect(self.sendMessage)
        self.chat_thread = ChatThread(role="stuff")  # pass client role
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

# information page
class informationPage(QMainWindow):
    def __init__(self):
        super(informationPage, self).__init__()
        uic.loadUi("./UI/information_page.ui", self)
        self.map_button.clicked.connect(self.map_page_function)
        self.appointments_button.clicked.connect(self.appointments_page_function)
        self.back_button.clicked.connect(self.back_function)

    def map_page_function(self):
        create_map_page = mapPage()
        widget.addWidget(create_map_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def appointments_page_function(self):
        create_appointments_page = appointmentsPage()
        widget.addWidget(create_appointments_page)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def back_function(self):
        widget.removeWidget(widget.currentWidget())

# map page
class mapPage(QMainWindow):
    def __init__(self):
        super(mapPage, self).__init__()
        uic.loadUi("./UI/map_page.ui", self)
        self.back_button.clicked.connect(self.back_function)

    def back_function(self):
        widget.removeWidget(widget.currentWidget())

# appointments page
class appointmentsPage(QMainWindow):
    def __init__(self):
        super(appointmentsPage, self).__init__()
        uic.loadUi("./UI/appointments_page.ui", self)
        self.back_button.clicked.connect(self.back_function)
        self.chat.clicked.connect(self.chat_function)

    def back_function(self):
        widget.removeWidget(widget.currentWidget())

    def chat_function(self):
        # send notification to the workers
        patient = notify.Patient("localhost", 12346)
        patient.notify_workers()
        patient.close()
        create_waiting_widget = chatWaitingWidget()
        widget.addWidget(create_waiting_widget)
        widget.setCurrentIndex(widget.currentIndex()+1)



app = QApplication(sys.argv)
landing_page = landingPage()
widget = QtWidgets.QStackedWidget()
widget.addWidget(landing_page)
widget.show()
app.exec_()
