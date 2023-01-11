import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QPixmap, QCursor
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5 import uic
import notify

# Landing page
class landingPage(QMainWindow):
    def __init__(self):
        super(landingPage, self).__init__()
        uic.loadUi("./UI/first_page.ui", self)
        self.chat.clicked.connect(self.chat_function)
        self.staff_login.clicked.connect(self.login_function)

    def chat_function(self):
        # send notification to the workers
        patient = notify.Patient("localhost", 55556)
        patient.notify_workers()
        patient.close()

    def login_function(self):
        create_login_page = loginPage()
        widget.addWidget(create_login_page)
        widget.setCurrentIndex(widget.currentIndex()+1)

# Login page
class loginPage(QMainWindow):
    def __init__(self):
        super(loginPage, self).__init__()
        uic.loadUi("./UI/login_page.ui", self)
        self.back_button.clicked.connect(self.back_function)
        self.login.clicked.connect(self.staff_page_function)

    def back_function(self):
        widget.setCurrentIndex(widget.currentIndex()-1)

    def staff_page_function(self):
        create_staff_page = staffPage()
        widget.addWidget(create_staff_page)
        widget.setCurrentIndex(widget.currentIndex()+1)

# staff page
class staffPage(QMainWindow):
    def __init__(self):
        super(staffPage, self).__init__()
        uic.loadUi("./UI/staff_page.ui", self)
        self.patient_waiting_number.setText(str(0))




app = QApplication(sys.argv)
landing_page = landingPage()
widget = QtWidgets.QStackedWidget()
widget.addWidget(landing_page)
widget.show()
app.exec_()