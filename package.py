import subprocess

# Define the package name you want to install
PyQt5_package = "PyQt5"
PyQt5_sip_package = "PyQt5-sip"
PyQt5_stubs_package = "PyQt5-stubs"
PyQt5_Qt5_package = "PyQt5-Qt5"
tkinter_package = "tkinter_package"


# Use pip to install the package
subprocess.check_call(["pip", "install", PyQt5_package])
subprocess.check_call(["pip", "install", PyQt5_sip_package])
subprocess.check_call(["pip", "install", PyQt5_stubs_package])
subprocess.check_call(["pip", "install", PyQt5_Qt5_package])
