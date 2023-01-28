import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QCursor
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5 import uic
import notify
from PyQt5.QtCore import QTimer
import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

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
        try:
            patient = notify.notifier("localhost", 12346)
            patient.notify()
            patient.close()
            create_waiting_widget = chatWaitingWidget()
            widget.addWidget(create_waiting_widget)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            print("server down")


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
            self.staff_page_function()
            pass

# staff page
class staffPage(QMainWindow):
    def __init__(self):
        super(staffPage, self).__init__()
        uic.loadUi("./UI/staff_page.ui", self)
        self.worker = notify.notified("localhost", 12346)
        self.worker.start()
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateChatRequest)
        self.timer.start(2000)  # 1000 ms = 1 second

    def updateChatRequest(self):

        if self.worker.notification_flag == 1:
            self.patient_waiting_number.setText(str(1))
            self.answer.clicked.connect(self.enterChat)
            self.worker.notification_flag = 0

    def enterChat(self):
            worker = notify.notifier("localhost", 12348)
            worker.notify()
            worker.close()
            ChatPage('127.0.0.2', 9090, 'stuff_member')


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
        self.patient = notify.notified("localhost", 12348)
        self.patient.start()
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
        if self.patient.notification_flag == 1:
            ChatPage('127.0.0.2', 9090, 'patient')
            self.patient.notification_flag = 0

class ChatPage:
    def __init__(self, host, port, nickname):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        self.nickname = nickname

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")
        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)
        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')
        self.message_label = tkinter.Label(self.win, text="Message:", bg="lightgray")
        self.message_label.config(font=("Arial", 12))
        self.message_label.pack(padx=20, pady=5)
        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)
        self.send_button = tkinter.Button(self.win, text="Send", command=self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5)
        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break

# information page
class informationPage(QMainWindow):
    def __init__(self):
        super(informationPage, self).__init__()
        uic.loadUi("./UI/information_page.ui", self)
        self.map_button.clicked.connect(self.map_page_function)
        self.back_button.clicked.connect(self.back_function)

    def map_page_function(self):
        create_map_page = mapPage()
        widget.addWidget(create_map_page)
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



app = QApplication(sys.argv)
landing_page = landingPage()
widget = QtWidgets.QStackedWidget()
widget.addWidget(landing_page)
widget.show()
app.exec_()
