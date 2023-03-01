import sys
from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

# start the first instance of the program
process1 = QProcess()
process1.start("python", ["app.py"]) # or the command that runs your script

# start the second instance of the program
process2 = QProcess()
process2.start("python", ["app.py"]) # or the command that runs your script
with open('./server.py') as server:
    server = server.read()
    exec(server)
app.exec_()

