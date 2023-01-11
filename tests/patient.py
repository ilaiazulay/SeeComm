import notify

if __name__ == "__main__":
    patient = notify.Patient("localhost", 55556)
    patient.notify_workers()
    patient.close()
