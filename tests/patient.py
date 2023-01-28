import notify

if __name__ == "__main__":
    patient = notify.notifier("localhost", 55556)
    patient.notify()
    patient.close()
